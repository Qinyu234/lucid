from src.schema.io import merge_io_seq, merge_io_router, normalize_io


def attach_children(node, proposal, topology: str, boundary: dict | None = None):

    if not proposal:
        return

    node["topology"] = topology
    node.setdefault("children", [])

    for p in proposal:

        child = {
            "semantic": p.get("semantic", ""),
            "function_name": p.get("function_name", ""),
            "children": [],
            "status": "growing",
            "role": "leaf",
            "code_path": p.get("code_path") or "",
            "topology": None,
            "tag": p.get("tag"),
            "case": p.get("case"),
            "io": normalize_io(p.get("io")),
            "code_ok": None,
        }

        node["children"].append(child)

    merged = merge_io_router(node["children"]) if topology == "ROUTER" else merge_io_seq(node["children"])

    if boundary and boundary.get("io"):
        bio = normalize_io(boundary["io"])
        if bio["in"]:
            merged["in"] = bio["in"]
        if bio["out"]:
            merged["out"] = bio["out"]

    node["io"] = merged
