"""
schema_accessor.py

THE ONLY FILE ALLOWED TO REFERENCE SCHEMA FIELD NAMES DIRECTLY.

All other code calls these functions.
When schema changes: update here only.

Rule: if you find yourself writing  obj["template_id"]  anywhere outside
this file, you are doing it wrong.
"""

from __future__ import annotations
from typing import Any


# ─────────────────────────────────────────────
# Primitives
# ─────────────────────────────────────────────

def get_id(obj: dict) -> str:
    return obj["id"]

def get_version(obj: dict) -> str:
    return obj["version"]

def get_schema_version(obj: dict) -> str:
    return obj["schema_version"]

def get_description(obj: dict) -> str:
    return obj.get("description", "")


# ─────────────────────────────────────────────
# Port schema
# ─────────────────────────────────────────────

def get_shape(port_schema: dict) -> str:
    return port_schema["shape"]

def get_items_schema(port_schema: dict) -> dict:
    return port_schema["items"]

def get_fields(port_schema: dict) -> dict:
    return port_schema.get("fields", {})

def get_enum_values(port_schema: dict) -> list[str]:
    return port_schema["values"]

def get_union_variants(port_schema: dict) -> list[str]:
    return port_schema["variants"]

def get_constraints(port_schema: dict) -> dict:
    return port_schema.get("constraints", {})

def is_port_required(port: dict) -> bool:
    return port.get("required", True)

def get_port_schema(port: dict) -> dict:
    return port["schema"]

def get_port_default(port: dict) -> Any:
    return port.get("default")


# ─────────────────────────────────────────────
# Node
# ─────────────────────────────────────────────

def get_node_type(node: dict) -> str:
    return node["type"]

def get_node_inputs(node: dict) -> dict:
    return node.get("inputs", {})

def get_node_outputs(node: dict) -> dict:
    return node.get("outputs", {})

def get_node_tags(node: dict) -> list[str]:
    return node.get("tags", [])

def get_node_params(node: dict) -> dict:
    return node.get("params", {})

# functional node
def get_template_id(node: dict) -> str:
    return node["template_id"]

def get_template_version(node: dict) -> str:
    return node["template_version"]

# control node
def get_control_kind(node: dict) -> str:
    return node["kind"]

def get_children(node: dict) -> list[str]:
    return node.get("children", [])

def get_condition_port(node: dict) -> str | None:
    return node.get("condition_port")

def get_branches(node: dict) -> dict:
    return node.get("branches", {})

def get_default_branch(node: dict) -> str | None:
    return node.get("default_branch")

def get_iterator_port(node: dict) -> str | None:
    return node.get("iterator_port")

def get_loop_body(node: dict) -> str | None:
    return node.get("body")

def get_termination(node: dict) -> dict:
    return node.get("termination", {})

# macro node
def get_macro_id(node: dict) -> str:
    return node["macro_id"]

def get_macro_version(node: dict) -> str:
    return node["macro_version"]


# ─────────────────────────────────────────────
# Edge
# ─────────────────────────────────────────────

def get_edge_from_node(edge: dict) -> str:
    return edge["from_node"]

def get_edge_from_port(edge: dict) -> str:
    return edge["from_port"]

def get_edge_to_node(edge: dict) -> str:
    return edge["to_node"]

def get_edge_to_port(edge: dict) -> str:
    return edge["to_port"]

def get_edge_coerce(edge: dict) -> dict | None:
    return edge.get("coerce")

def get_coerce_safety(coerce: dict) -> str:
    return coerce["safety"]

def get_coerce_fn(coerce: dict) -> str | None:
    return coerce.get("coerce_fn")


# ─────────────────────────────────────────────
# Graph
# ─────────────────────────────────────────────

def get_root_id(graph: dict) -> str:
    return graph["root_id"]

def get_nodes(graph: dict) -> dict:
    return graph["nodes"]

def get_edges(graph: dict) -> dict:
    return graph["edges"]

def get_node_by_id(graph: dict, node_id: str) -> dict | None:
    return graph["nodes"].get(node_id)

def get_edge_by_id(graph: dict, edge_id: str) -> dict | None:
    return graph["edges"].get(edge_id)

def get_graph_metadata(graph: dict) -> dict:
    return graph.get("metadata", {})


# ─────────────────────────────────────────────
# Template
# ─────────────────────────────────────────────

def get_template_inputs(template: dict) -> dict:
    return template["inputs"]

def get_template_outputs(template: dict) -> dict:
    return template["outputs"]

def get_implementations(template: dict) -> dict:
    return template["implementations"]

def get_implementation(template: dict, lang: str) -> dict | None:
    return template["implementations"].get(lang)

def get_code_file(impl: dict) -> str:
    return impl["code_file"]

def get_impl_deps(impl: dict) -> list[str]:
    return impl.get("deps", [])

def get_test_suite(template: dict) -> dict:
    return template["tests"]

def get_fixed_cases(test_suite: dict) -> list:
    return test_suite["fixed_cases"]

def get_generated_rules(test_suite: dict) -> dict:
    return test_suite["generated_rules"]

def get_template_tags(template: dict) -> list[str]:
    return template.get("tags", [])


# ─────────────────────────────────────────────
# Test case
# ─────────────────────────────────────────────

def get_case_inputs(case: dict) -> dict:
    return case["inputs"]

def get_case_expect(case: dict) -> dict:
    return case["expect"]

def get_expected_outputs(expect: dict) -> dict:
    return expect.get("outputs", {})

def get_expected_properties(expect: dict) -> list[str]:
    return expect.get("properties", [])

def expects_error(expect: dict) -> bool:
    return expect.get("error", False)

def get_case_tags(case: dict) -> list[str]:
    return case.get("tags", [])


# ─────────────────────────────────────────────
# Operation
# ─────────────────────────────────────────────

def get_op_id(op: dict) -> str:
    return op["op_id"]

def get_op_type(op: dict) -> str:
    return op["op"]

def get_op_graph_id(op: dict) -> str:
    return op["graph_id"]

def get_op_author(op: dict) -> str:
    return op["author"]

def get_op_parent(op: dict) -> str | None:
    return op["parent_op_id"]

def is_op_online(op: dict) -> bool:
    return op.get("online", True)

def is_op_reversible(op: dict) -> bool:
    return op.get("reversible", True)

def get_op_result(op: dict) -> str:
    return op.get("result", "pending")

def get_op_payload(op: dict) -> dict:
    """Return the operation-specific payload fields."""
    base_keys = {
        "op_id", "parent_op_id", "op", "graph_id",
        "author", "session_id", "timestamp", "online",
        "reversible", "result", "reject_reason"
    }
    return {k: v for k, v in op.items() if k not in base_keys}
