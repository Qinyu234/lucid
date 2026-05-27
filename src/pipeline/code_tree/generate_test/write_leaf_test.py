def write_leaf_test(node: dict, job_id=None) -> bool:
    from src.shared.lib.write_leaf_test_util import write_leaf_test_util

    return write_leaf_test_util(node, job_id)
