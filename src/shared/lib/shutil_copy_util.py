def shutil_copy_util(src: str, dst: str) -> None:
    import shutil

    shutil.copy2(src, dst)
