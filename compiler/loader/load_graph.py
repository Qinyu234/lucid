"""
load_graph.py

Load graph from graph/l1/latest.json and validate against graph.schema.json.
Returns graph dict accessed through schema_accessor functions.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any

from compiler.accessor.schema_accessor import (
    get_root_id,
    get_nodes,
    get_edges,
    get_graph_metadata,
    get_schema_version,
)


def load_graph(graph_path: str | Path = "graph/l1/latest.json") -> dict[str, Any]:
    """
    Load graph from JSON file and validate basic structure.
    
    Args:
        graph_path: Path to graph JSON file
        
    Returns:
        Graph dictionary
        
    Raises:
        FileNotFoundError: If graph file doesn't exist
        json.JSONDecodeError: If graph file is not valid JSON
        ValueError: If graph structure is invalid
    """
    graph_path = Path(graph_path)
    
    if not graph_path.exists():
        raise FileNotFoundError(f"Graph file not found: {graph_path}")
    
    with open(graph_path, "r", encoding="utf-8") as f:
        graph = json.load(f)
    
    # Basic validation
    if not isinstance(graph, dict):
        raise ValueError("Graph must be a dictionary")
    
    # Validate required fields exist (using accessor functions)
    try:
        root_id = get_root_id(graph)
        nodes = get_nodes(graph)
        edges = get_edges(graph)
        schema_version = get_schema_version(graph)
    except KeyError as e:
        raise ValueError(f"Graph missing required field: {e}")
    
    # Validate types
    if not isinstance(root_id, str):
        raise ValueError("root_id must be a string")
    
    if not isinstance(nodes, dict):
        raise ValueError("nodes must be a dictionary")
    
    if not isinstance(edges, dict):
        raise ValueError("edges must be a dictionary")
    
    # Validate root_id exists in nodes
    if root_id not in nodes:
        raise ValueError(f"root_id '{root_id}' not found in nodes")
    
    return graph


def load_graph_with_metadata(graph_path: str | Path = "graph/l1/latest.json") -> dict[str, Any]:
    """
    Load graph and include metadata.
    
    Args:
        graph_path: Path to graph JSON file
        
    Returns:
        Dictionary with 'graph' and 'metadata' keys
    """
    graph = load_graph(graph_path)
    metadata = get_graph_metadata(graph)
    
    return {
        "graph": graph,
        "metadata": metadata,
    }
