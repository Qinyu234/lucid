def build_registry(tasks: list[dict]) -> dict:
    registry = {}

    for t in tasks:
        key = t.get("file_path") or t["file_name"].replace(".py", "")
        registry[key] = t

    return registry