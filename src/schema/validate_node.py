from copy import deepcopy

from src.schema.engine import load_schema, validate
from src.schema.io.normalize_io import normalize_io
from src.schema.io.normalize_node import normalize_node


def validate_node(node: dict, strict: bool = False):
    prepared = normalize_node(deepcopy(node))
    prepared.setdefault("children", [])
    prepared.setdefault("code_path", "")
    schema = load_schema("node_schema.json")
    result = validate(prepared, schema)

    if strict and prepared.get("status") == "growing" and prepared.get("children"):
        result.fail("$.children: growing node must not have children yet")

    return result, prepared
