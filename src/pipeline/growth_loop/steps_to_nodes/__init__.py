from ..assign_topology import build_case_map
from .generate_function_name import generate_function_name
from src.schema.io import empty_io, normalize_io


def steps_to_nodes(steps: list) -> list:

    case_map = build_case_map(steps)
    children = []

    for step in steps:

        semantic = step["semantic"]

        node = {
            "semantic": semantic,
            "function_name": None,
            "children": [],
            "status": "growing",
            "role": "leaf",
            "code_path": None,
            "topology": None,
            "tag": step.get("tag"),
            "case": None,
            "io": normalize_io(step.get("io")),
            "code_ok": None,
        }

        if step.get("tag") and case_map:
            node["case"] = case_map.get(step["tag"])

        name = generate_function_name(node)

        if not isinstance(name, str) or name.strip() == "":
            name = "node_" + str(abs(hash(semantic)))[:8]

        node["function_name"] = name
        children.append(node)

    return children
