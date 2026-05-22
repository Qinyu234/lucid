import logging

from src.log import get_logger, log_event
from src.memory import register_leaf

from .generate_code import generate_code
from .write_file import write_file
from .render_init import render_init


def code_tree(root, job_id=None):

    logger = get_logger(job_id)
    log_event(logger, "code_tree_start")

    stack = [root]

    while stack:

        node = stack.pop()
        children = node.get("children", [])
        path = node["code_path"]

        if children:

            code = render_init(node)
            out_path = f"{path}/__init__.py"
            write_file(out_path, code)

            log_event(
                logger,
                "code_tree_write_init",
                path=out_path,
                topology=node.get("topology"),
                io=node.get("io"),
            )

            for child in children:
                child_fn = child.get("function_name") or "unnamed"
                child["code_path"] = f"{path}/{child_fn}"
                stack.append(child)

            continue

        code = generate_code(node, job_id=job_id)

        if not code:
            log_event(
                logger,
                "code_tree_leaf_empty",
                level=logging.ERROR,
                path=path,
                semantic=node.get("semantic"),
            )
            continue

        out_path = f"{path}.py"
        write_file(out_path, code)
        register_leaf(node, code, out_path)

        log_event(
            logger,
            "code_tree_write_leaf",
            path=out_path,
            io=node.get("io"),
        )
