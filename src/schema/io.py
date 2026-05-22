# Node dataflow: io.in / io.out name keys in ctx["data"]


def empty_io():
    return {"in": [], "out": []}


def _keys(lst) -> list:
    if not isinstance(lst, list):
        return []
    return sorted({str(k).strip() for k in lst if k and str(k).strip()})


def normalize_io(raw) -> dict:
    if not isinstance(raw, dict):
        return empty_io()

    if "in" in raw or "out" in raw:
        return {"in": _keys(raw.get("in")), "out": _keys(raw.get("out"))}

    if "data_keys" in raw:
        return {"in": _keys(raw.get("data_keys")), "out": _keys(raw.get("data_keys"))}

    return empty_io()


def normalize_node(node: dict) -> dict:
    if "io" in node:
        node["io"] = normalize_io(node["io"])
        return node

    if "input" in node or "output" in node:
        inp = node.pop("input", {})
        out = node.pop("output", {})
        in_keys = _keys(inp.get("data_keys", [])) if isinstance(inp, dict) else []
        out_keys = _keys(out.get("data_keys", [])) if isinstance(out, dict) else []
        node["io"] = {"in": in_keys, "out": out_keys}
        return node

    node["io"] = empty_io()
    return node


def merge_io_seq(children: list) -> dict:
    if not children:
        return empty_io()
    first = normalize_io(children[0].get("io"))
    last = normalize_io(children[-1].get("io"))
    return {"in": first["in"], "out": last["out"]}


def merge_io_router(children: list) -> dict:
    if not children:
        return empty_io()
    ins, outs = set(), set()
    for child in children:
        io = normalize_io(child.get("io"))
        ins.update(io["in"])
        outs.update(io["out"])
    return {"in": sorted(ins), "out": sorted(outs)}
