"""
002_validate_edges.py

Validate that edge from_node/to_node exist.
Validate that from_port/to_port exist in corresponding node's inputs/outputs.
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
)


def run_pass(graph: dict[str, Any], meta: dict[str, Any]) -> dict[str, Any]:
    """
    Validate all edges in graph.
    
    Args:
        graph: Graph dictionary
        meta: Metadata dictionary
        
    Returns:
        Dictionary with 'errors', 'warnings', 'graph' keys
    """
    errors = []
    warnings = []
    
    nodes = get_nodes(graph)
    edges = get_edges(graph)
    
    for edge_id, edge in edges.items():
        from_node_id = get_edge_from_node(edge)
        to_node_id = get_edge_to_node(edge)
        from_port = get_edge_from_port(edge)
        to_port = get_edge_to_port(edge)
        
        # Validate from_node exists
        from_node = get_node_by_id(graph, from_node_id)
        if from_node is None:
            errors.append(f"Edge '{edge_id}': from_node '{from_node_id}' does not exist")
            continue
        
        # Validate to_node exists
        to_node = get_node_by_id(graph, to_node_id)
        if to_node is None:
            errors.append(f"Edge '{edge_id}': to_node '{to_node_id}' does not exist")
            continue
        
        # Validate from_port exists in from_node's outputs
        from_node_outputs = get_node_outputs(from_node)
        if from_port not in from_node_outputs:
            errors.append(
                f"Edge '{edge_id}': from_port '{from_port}' not in from_node '{from_node_id}' outputs: {list(from_node_outputs.keys())}"
            )
        
        # Validate to_port exists in to_node's inputs
        to_node_inputs = get_node_inputs(to_node)
        if to_port not in to_node_inputs:
            errors.append(
                f"Edge '{edge_id}': to_port '{to_port}' not in to_node '{to_node_id}' inputs: {list(to_node_inputs.keys())}"
            )
    
    return {
        "errors": errors,
        "warnings": warnings,
        "graph": graph,
    }
