def child_code_path(parent_path: str, function_name: str) -> str:
    from src.shared.io_tree.child_code_path_util import child_code_path_util

    return child_code_path_util(parent_path, function_name)
