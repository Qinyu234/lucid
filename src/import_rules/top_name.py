def top_name(module: str | None) -> str:
    if not module:
        return ""
    return module.split(".")[0]
