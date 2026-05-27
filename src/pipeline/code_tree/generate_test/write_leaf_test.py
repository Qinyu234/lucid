def write_leaf_test(node: dict, job_id=None) -> bool:
    import logging

    from src.pipeline.code_tree.generate_test.render_test import render_test
    from src.pipeline.code_tree.generate_test.test_path_for_leaf import test_path_for_leaf
    from src.pipeline.code_tree.generate_test.tests_enabled import tests_enabled
    from src.pipeline.code_tree.generate_test.verify_test import verify_test
    from src.pipeline.code_tree.write_file import write_file
    from src.shared.logging.event_util import event_util
    from src.shared.logging.get_logger_util import get_logger_util

    if not tests_enabled():
        return False
    logger = get_logger_util(job_id)
    fn = node.get("function_name") or "module"
    code_path = node.get("code_path") or fn
    code = render_test(node)
    ok, err = verify_test(code, fn)
    if not ok:
        node["test_ok"] = False
        event_util(
            logger,
            "code_tree_test_verify_fail",
            level=logging.ERROR,
            function_name=fn,
            error=err,
        )
        return False
    out_path = test_path_for_leaf(code_path, fn)
    write_file(out_path, code)
    node["test_ok"] = True
    event_util(logger, "code_tree_write_test", path=out_path, function_name=fn)
    return True
