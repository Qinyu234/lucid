def is_fully_grown_util(node) -> bool:
    status = node.get("status")
    if status in ("growing", "failed"):
        return False
    if status != "done":
        return False
    for child in node.get("children", []):
        if not is_fully_grown_util(child):
            return False
    return True
