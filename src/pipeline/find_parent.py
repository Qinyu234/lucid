def find_parent(root: dict, target: dict, parent: dict | None = None) -> dict | None:
    if root is target:
        return parent

    for child in root.get("children", []):
        if child is target:
            return root
        found = find_parent(child, target, root)
        if found is not None:
            return found

    return None
