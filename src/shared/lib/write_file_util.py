def write_file_util(path: str, code: str) -> None:
    from src.shared.lib.path_write_text_util import path_write_text_util

    path_write_text_util(path, code)
