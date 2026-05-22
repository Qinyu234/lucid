from src.schema.io import normalize_io


def context_builder(node):

    io = normalize_io(node.get("io"))

    return {
        "semantic": node["semantic"],
        "children_count": len(node.get("children", [])),
        "io_in": io["in"],
        "io_out": io["out"],
    }
