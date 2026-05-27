def path_is_file_util(path: str) -> bool:
    from pathlib import Path

    return Path(path).is_file()

