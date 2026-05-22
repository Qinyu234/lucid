def is_fully_grown(node):

    # =========================
    # 1. current node check
    # =========================
    if node.get("status") != "done":
        return False

    # =========================
    # 2. leaf check
    # =========================
    children = node.get("children", [])

    for child in children:

        if not is_fully_grown(child):

            return False

    return True