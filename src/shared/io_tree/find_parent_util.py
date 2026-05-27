def find_parent_util(root: dict, target: dict, parent: dict | None = None) -> dict | None:
    if root is target:
        return parent
    for child in root.get("children", []):
        if child is target:
            return root
        found = find_parent_util(child, target, root)
        if found is not None:
            return found
    return None

