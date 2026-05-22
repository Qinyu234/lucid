def context_builder(node):

    # =========================
    # default minimal context
    # =========================
    ctx = {
        "semantic": node["semantic"],
        "children_count": len(node.get("children", [])),
    }

    # =========================
    # future expansion hook
    # =========================
    # - sibling context
    # - parent context
    # - global graph context
    # - dependency context

    return ctx