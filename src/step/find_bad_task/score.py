def score(task: dict) -> float:
    # 完整性
    s = 0.0

    if task.get("file_name"):
        s += 0.3

    if task.get("functions"):
        s += 0.3

    if task.get("imports") is not None:
        s += 0.2

    if task.get("semantic"):
        s += 0.2

    return s