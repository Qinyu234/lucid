def path_read_text_util(path: str, encoding: str = "utf-8") -> str:
    from pathlib import Path

    return Path(path).read_text(encoding=encoding)

