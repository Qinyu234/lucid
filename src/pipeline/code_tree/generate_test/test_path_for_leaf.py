def test_path_for_leaf(code_path: str, function_name: str) -> str:
    from src.shared.lib.test_path_for_leaf_util import test_path_for_leaf_util

    return test_path_for_leaf_util(code_path, function_name)
