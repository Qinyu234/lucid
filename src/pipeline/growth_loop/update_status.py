# =========================
# FUNCTION:
# update_status
#
# PURPOSE:
# control lifecycle of node
# =========================


def update_status(node):

    task = node.get("task", {})

    active = task.get("active", [])

    children = node.get("children", [])

    retry = node.get("retry", 0)

    # =====================
    # 1. retry-based cutoff
    # =====================

    if retry >= 3:

        node["status"] = "done"
        return

    # =====================
    # 2. no active work
    # =====================

    if not active:

        node["status"] = "done"
        return

    # =====================
    # 3. already expanded
    # =====================

    if children and len(children) > 0:

        node["status"] = "done"
        return

    # =====================
    # default
    # =====================

    node["status"] = "growing"