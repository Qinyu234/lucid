from copy import deepcopy

from .engine import load_schema, validate
from .io import empty_io, normalize_io, normalize_node


def validate_node(node: dict, strict: bool = False):
    prepared = normalize_node(deepcopy(node))
    prepared.setdefault("children", [])
    prepared.setdefault("code_path", "")
    schema = load_schema("node_schema.json")
    result = validate(prepared, schema)

    if strict and prepared.get("status") == "growing" and prepared.get("children"):
        result.fail("$.children: growing node must not have children yet")

    return result, prepared


def validate_expand_output(data: dict):
    schema = load_schema("expand_schema.json")
    return validate(data, schema)


def validate_job_input(data: dict):
    schema = load_schema("data_schema.json")
    return validate(data, schema)
