import os


def write_file(path, code):

    # =========================
    # 1. ensure directory exists
    # =========================
    dir_path = os.path.dirname(path)

    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    # =========================
    # 2. write file
    # =========================
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)