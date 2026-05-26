from src.shared.load_app_config import load_app_config
from src.shared.get_logger import get_logger
from src.shared.log_event import log_event
from .compile_module import compile_module
from .generate_code import generate_code
from .write_file import write_file
from .render_init import render_init
from .render_init_minimal import render_init_minimal

def code_tree(root, job_id=None, job=None):
    import logging
    from src.pipeline.memory.register_leaf import register_leaf
    from .generate_test.ensure_conftest import ensure_conftest
    from .generate_test.write_leaf_test import write_leaf_test
    from .generate_code.verify_code import verify_code

    def postorder(node):
        ordered = []
        for child in node.get('children', []):
            ordered.extend(postorder(child))
        ordered.append(node)
        return ordered

    def needs_code(node):
        return node.get('code_ok') is not True

    def emit_leaf(node):
        path = node.get('code_path') or ''
        code = generate_code(node, job_id=job_id, root=root)
        if not code:
            node['code_ok'] = False
            log_event(logger, 'code_tree_leaf_empty', level=logging.ERROR, path=path, function_name=node.get('function_name'))
            return False
        out_path = f'{path}.py'
        write_file(out_path, code)
        if compile_check:
            cok, cerr = compile_module(out_path)
            if not cok:
                node['code_ok'] = False
                log_event(logger, 'code_tree_leaf_compile_fail', level=logging.ERROR, path=out_path, error=cerr)
                return False
        register_leaf(node, code, out_path)
        write_leaf_test(node, job_id=job_id)
        node['code_ok'] = True
        log_event(logger, 'code_tree_write_leaf', path=out_path, code_kind=node.get('code_kind'))
        return True

    def emit_composite(node):
        path = node.get('code_path') or ''
        code = render_init(node)
        ok, err = verify_code(code, node)
        if not ok and stub_on_fail:
            code = render_init_minimal(node)
            ok, err = verify_code(code, node)
            if ok:
                node['code_kind'] = 'stub'
                log_event(logger, 'code_tree_init_stub_fallback', level=logging.WARNING, path=path, error=err)
        if not ok:
            node['code_ok'] = False
            log_event(logger, 'code_tree_init_verify_fail', level=logging.ERROR, path=path, function_name=node.get('function_name'), error=err)
            return False
        init_path = f'{path}/__init__.py'
        write_file(init_path, code)
        if compile_check:
            cok, cerr = compile_module(init_path)
            if not cok:
                node['code_ok'] = False
                log_event(logger, 'code_tree_init_compile_fail', level=logging.ERROR, path=init_path, error=cerr)
                return False
        node['code_ok'] = True
        node.setdefault('code_kind', 'template')
        log_event(logger, 'code_tree_write_init', path=init_path)
        return True
    logger = get_logger(job_id)
    cfg = load_app_config().get('codegen', {})
    compile_check = cfg.get('compile_check', True)
    stub_on_fail = cfg.get('stub_on_fail', True)
    max_passes = int(cfg.get('max_tree_passes', 10))
    log_event(logger, 'code_tree_start', max_passes=max_passes)
    ensure_conftest(job, job_id=job_id)
    ordered = postorder(root)
    pass_num = 0
    while pass_num < max_passes:
        pending = [n for n in ordered if needs_code(n)]
        if not pending:
            log_event(logger, 'code_tree_converged', passes=pass_num)
            break
        log_event(logger, 'code_tree_pass', pass_num=pass_num, pending=len(pending))
        for node in pending:
            children = node.get('children', [])
            path = node.get('code_path') or ''
            if not children:
                if node.get('status') == 'failed' and (not stub_on_fail):
                    node['code_ok'] = False
                    continue
                emit_leaf(node)
                continue
            child_ok = all((c.get('code_ok') is True for c in children))
            if not child_ok:
                log_event(logger, 'code_tree_composite_wait_children', level=logging.WARNING, path=path, function_name=node.get('function_name'))
                continue
            emit_composite(node)
        pass_num += 1
    still_pending = [n for n in ordered if needs_code(n)]
    if still_pending:
        log_event(logger, 'code_tree_incomplete', level=logging.WARNING, pending=len(still_pending), max_passes=max_passes)
