def attach_children(node, proposal, assignment: dict, boundary: dict | None = None):
    from src.shared.io_tree.child_code_path_util import child_code_path_util
    from src.shared.validate.io_merge_router_util import io_merge_router_util
    from src.shared.validate.io_merge_seq_util import io_merge_seq_util
    from src.shared.validate.io_normalize_util import io_normalize_util

    def dedupe_sibling_names(children: list) -> list:
        used: set[str] = set()
        for child in children:
            fn = child.get("function_name") or "unnamed"
            base = fn
            if fn in used:
                idx = 2
                while f"{base}_{idx}" in used:
                    idx += 1
                fn = f"{base}_{idx}"
                child["function_name"] = fn
            used.add(fn)
        return children

    if not proposal:
        return
    topology = str(assignment.get("topology") or "SEQ")
    node["topology"] = topology
    node["template_id"] = assignment.get("template_id")
    node["topology_tree"] = assignment.get("tree")
    node.setdefault("children", [])
    parent_path = (node.get("code_path") or "").rstrip("/\\")
    parent_depth = node.get("depth", 0)
    for p in proposal:
        fn = p.get("function_name") or "unnamed"
        child = {
            "semantic": p.get("semantic", ""),
            "function_name": fn,
            "children": [],
            "status": "growing",
            "role": "leaf",
            "code_path": child_code_path_util(parent_path, fn),
            "depth": parent_depth + 1,
            "topology": None,
            "tag": p.get("tag"),
            "case": p.get("case"),
            "io": io_normalize_util(p.get("io")),
            "code_ok": None,
        }
        node["children"].append(child)
    dedupe_sibling_names(node["children"])
    for child in node["children"]:
        child["code_path"] = child_code_path_util(parent_path, child["function_name"])
    if topology == "ROUTER":
        for i, child in enumerate(node["children"]):
            if not child.get("case"):
                child["case"] = f"CASE_{i}"
            if not child.get("tag"):
                child["tag"] = child.get("case")
    merged = (
        io_merge_router_util(node["children"])
        if topology == "ROUTER"
        else io_merge_seq_util(node["children"])
    )
    if boundary and boundary.get("io"):
        bio = io_normalize_util(boundary["io"])
        if bio["in"]:
            merged["in"] = bio["in"]
        if bio["out"]:
            merged["out"] = bio["out"]
    node["io"] = merged
