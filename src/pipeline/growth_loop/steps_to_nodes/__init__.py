from ..build_case_map import build_case_map
from .generate_function_name import generate_function_name
from src.schema.io.normalize_io import normalize_io


def steps_to_nodes(steps: list, job_id=None) -> list:

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

        node["function_name"] = generate_function_name(node, job_id=job_id)
        children.append(node)

    return children
