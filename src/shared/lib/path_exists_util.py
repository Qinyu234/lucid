def path_exists_util(path: str) -> bool:
    from pathlib import Path

    return Path(path).exists()

