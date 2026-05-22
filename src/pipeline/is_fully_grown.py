def is_fully_grown(node) -> bool:

    status = node.get("status")

    if status in ("growing", "failed"):
        return False

    if status != "done":
        return False

    for child in node.get("children", []):
        if not is_fully_grown(child):
            return False

    return True
