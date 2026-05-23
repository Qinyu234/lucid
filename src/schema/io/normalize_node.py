from src.schema.io.empty_io import empty_io
from src.schema.io.normalize_io import normalize_io


def normalize_node(node: dict) -> dict:
    if "io" in node:
        node["io"] = normalize_io(node["io"])
        return node

    if "input" in node or "output" in node:
        inp = node.pop("input", {})
        out = node.pop("output", {})
        node["io"] = normalize_io({
            "in": inp.get("data_keys", []) if isinstance(inp, dict) else [],
            "out": out.get("data_keys", []) if isinstance(out, dict) else [],
        })
        return node

    node["io"] = empty_io()
    return node
