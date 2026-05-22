def attach_children(node, proposal):

    if not proposal:
        return

    node.setdefault("children", [])

    for p in proposal:

        child = {

            # =====================
            # identity
            # =====================
            "semantic": p.get("semantic", ""),

            # =====================
            # structure
            # =====================
            "children": [],
            "status": "growing",

            # =====================
            # execution
            # =====================
            "code_path": p.get("code_path", ""),

        }

        node["children"].append(child)