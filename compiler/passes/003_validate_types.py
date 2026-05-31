"""
003_validate_types.py

Check io.schema.json coerce table for type compatibility between connected ports.
safe -> pass
unsafe -> pass, mark in edge.coerce
forbidden -> error, reject execution
"""

from __future__ import annotations
from typing import Any

from compiler.accessor.schema_accessor import (
    get_nodes,
    get_edges,
    get_node_by_id,
    get_edge_from_node,
    get_edge_from_port,
    get_edge_to_node,
    get_edge_to_port,
    get_node_inputs,
    get_node_outputs,
    get_port_schema,
    get_shape,
    get_edge_coerce,
)


def run_pass(graph: dict[str, Any], meta: dict[str, Any]) -> dict[str, Any]:
    """
    Validate type compatibility for all edges using coerce table.
    
    Args:
        graph: Graph dictionary
        meta: Metadata dictionary containing io_rules with coerce table
        
    Returns:
        Dictionary with 'errors', 'warnings', 'graph' keys
    """
    errors = []
    warnings = []
    
    nodes = get_nodes(graph)
    edges = get_edges(graph)
    
    # Get coerce table from io rules
    io_rules = meta.get("rules", {}).get("io_rules", {})
    coerce_table_usage = io_rules.get("coerce_table_usage", {})
    
    # For Phase 1, we'll do basic shape compatibility checking
    # Full coerce table lookup will be implemented when io.schema.json is complete
    
    for edge_id, edge in edges.items():
        from_node_id = get_edge_from_node(edge)
        to_node_id = get_edge_to_node(edge)
        from_port = get_edge_from_port(edge)
        to_port = get_edge_to_port(edge)
        
        from_node = get_node_by_id(graph, from_node_id)
        to_node = get_node_by_id(graph, to_node_id)
        
        if from_node is None or to_node is None:
            continue  # Already validated in 002_validate_edges
        
        from_node_outputs = get_node_outputs(from_node)
        to_node_inputs = get_node_inputs(to_node)
        
        from_port_schema = get_port_schema(from_node_outputs[from_port])
        to_port_schema = get_port_schema(to_node_inputs[to_port])
        
        from_shape = get_shape(from_port_schema)
        to_shape = get_shape(to_port_schema)
        
        # Basic type compatibility check
        if from_shape == to_shape:
            # Same shape - safe
            pass
        elif from_shape == "any" or to_shape == "any":
            warnings.append(f"Edge '{edge_id}': 'any' type used, should use explicit union")
        else:
            # Different shapes - check if coercion is allowed
            # For Phase 1, we'll mark as unsafe and continue
            # Full coerce table lookup will be added later
            warnings.append(
                f"Edge '{edge_id}': type coercion from '{from_shape}' to '{to_shape}' may be unsafe"
            )
            
            # Mark coerce in edge if not already present
            if get_edge_coerce(edge) is None:
                edge["coerce"] = {
                    "safety": "unsafe",
                    "from_shape": from_shape,
                    "to_shape": to_shape,
                }
    
    return {
        "errors": errors,
        "warnings": warnings,
        "graph": graph,
    }
