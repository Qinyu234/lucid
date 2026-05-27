def compile_module(path: str) -> tuple:
    from src.shared.lib.compile_module_util import compile_module_util

    return compile_module_util(path)
