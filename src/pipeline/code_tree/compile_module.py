def compile_module(path: str) -> tuple:
    from src.shared.lib.path_exists_util import path_exists_util
    from src.shared.lib.py_compile_util import py_compile_util

    if not path_exists_util(path):
        return False, f"file not found: {path}"
    return py_compile_util(path)
