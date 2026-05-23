import logging

from src.log.get_logger import get_logger
from src.log.log_event import log_event
from src.memory.register_leaf import register_leaf

from .generate_code import generate_code
from .generate_test.ensure_conftest import ensure_conftest
from .generate_test.write_leaf_test import write_leaf_test
from .write_file import write_file
from .render_init import render_init
from .generate_code.verify_code import verify_code


def code_tree(root, job_id=None, job=None):

    logger = get_logger(job_id)
    log_event(logger, "code_tree_start")

    ensure_conftest(job, job_id=job_id)

    stack = [root]

    while stack:

        node = stack.pop()
        children = node.get("children", [])
        path = node.get("code_path") or ""

        if children:

            code = render_init(node)
            ok, err = verify_code(code, node)

            if not ok:
                node["code_ok"] = False
                log_event(
                    logger,
                    "code_tree_init_verify_fail",
                    level=logging.ERROR,
                    path=path,
                    function_name=node.get("function_name"),
                    error=err,
                )
                for child in children:
                    stack.append(child)
                continue

            write_file(f"{path}/__init__.py", code)
            node["code_ok"] = True
            log_event(logger, "code_tree_write_init", path=f"{path}/__init__.py")

            for child in children:
                stack.append(child)
            continue

        if node.get("status") == "failed":
            node["code_ok"] = False
            continue

        code = generate_code(node, job_id=job_id, root=root)

        if not code:
            node["code_ok"] = False
            log_event(
                logger,
                "code_tree_leaf_empty",
                level=logging.ERROR,
                path=path,
                function_name=node.get("function_name"),
            )
            continue

        out_path = f"{path}.py"
        write_file(out_path, code)
        register_leaf(node, code, out_path)
        write_leaf_test(node, job_id=job_id)
        node["code_ok"] = True
        log_event(logger, "code_tree_write_leaf", path=out_path)
