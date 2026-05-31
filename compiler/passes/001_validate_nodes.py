"""
001_validate_nodes.py

Validate that all node template_ids are in operator_registry.
Validate that control node kinds are in legal set.
"""

from __future__ import annotations
from typing import Any

from compiler.accessor.schema_accessor import (
    get_nodes,
    get_node_type,
    get_template_id,
    get_control_kind,
)


def run_pass(graph: dict[str, Any], meta: dict[str, Any]) -> dict[str, Any]:
    """
    Validate all nodes in graph.
    
    Args:
        graph: Graph dictionary
        meta: Metadata dictionary containing operator_registry and rules
        
    Returns:
        Dictionary with 'errors', 'warnings', 'graph' keys
    """
    errors = []
    warnings = []
    
    nodes = get_nodes(graph)
    operator_registry = meta.get("operator_registry", {})
    topology_rules = meta.get("rules", {}).get("topology_rules", {})
    
    # Get legal control node kinds from topology rules
    legal_control_kinds = set(topology_rules.get("control_nodes", {}).keys())
    
    for node_id, node in nodes.items():
        node_type = get_node_type(node)
        
        if node_type == "functional":
            # Validate template_id exists in registry
            template_id = get_template_id(node)
            
            # Check if template is registered
            registered_templates = operator_registry.get("templates", {}).get("functional", {})
            
            if template_id not in registered_templates:
                errors.append(f"Node '{node_id}': template_id '{template_id}' not registered in operator_registry")
        
        elif node_type == "control":
            # Validate control kind is legal
            kind = get_control_kind(node)
            
            if kind not in legal_control_kinds:
                errors.append(f"Node '{node_id}': control kind '{kind}' not in legal set: {legal_control_kinds}")
        
        elif node_type == "macro":
            # Macro validation will be added in Phase 6
            warnings.append(f"Node '{node_id}': macro nodes not yet supported")
        
        else:
            errors.append(f"Node '{node_id}': unknown node type '{node_type}'")
    
    return {
        "errors": errors,
        "warnings": warnings,
        "graph": graph,
    }
