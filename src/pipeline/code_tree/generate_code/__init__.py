from src.shared.load_app_config import load_app_config
from src.shared.get_logger import get_logger
from src.shared.log_event import log_event
from .build_prompt import build_prompt
from .verify_code import verify_code

def generate_code(node, max_retry=None, job_id=None, root=None):
    import logging
    from src.llm import llm
    from src.pipeline.memory.recall_for_reuse import recall_for_reuse
    from src.pipeline.memory.render_reuse_wrapper import render_reuse_wrapper
    from src.pipeline.code_tree.render_leaf_stub import render_leaf_stub
    logger = get_logger(job_id)
    fn = node.get('function_name') or 'module'
    cfg = load_app_config().get('codegen', {})
    stub_on_fail = cfg.get('stub_on_fail', True)
    if max_retry is None:
        max_retry = int(cfg.get('max_retry', 6))
    for cand in recall_for_reuse(node, job_id=job_id):
        code = render_reuse_wrapper(node, cand['module'])
        ok, err = verify_code(code, node)
        if ok:
            node['code_kind'] = 'reuse'
            log_event(logger, 'memory_reuse_ok', module=cand.get('module'), rerank=cand.get('_rerank_score'))
            return code
        log_event(logger, 'memory_reuse_verify_fail', level=logging.WARNING, module=cand.get('module'), error=err)
    for attempt in range(max_retry):
        code = llm('code', build_prompt(node, root=root), job_id=job_id)
        ok, err = verify_code(code, node)
        if ok:
            node['code_kind'] = 'llm'
            return code
        log_event(logger, 'code_gen_verify_fail', level=logging.WARNING, attempt=attempt, error=err, function_name=fn)
    if stub_on_fail:
        stub = render_leaf_stub(node)
        ok, err = verify_code(stub, node)
        if ok:
            node['code_kind'] = 'stub'
            log_event(logger, 'code_gen_stub_fallback', level=logging.WARNING, function_name=fn, semantic=node.get('semantic'))
            return stub
        log_event(logger, 'code_gen_stub_invalid', level=logging.ERROR, error=err)
    log_event(logger, 'code_gen_exhausted', level=logging.ERROR, semantic=node.get('semantic'))
    return ''
