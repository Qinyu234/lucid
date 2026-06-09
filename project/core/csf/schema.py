"""
CSF (Canonical Structural Form) Schema
CSF is an explicit representation of implicit structure in code.
It is NOT an IR (Intermediate Representation) or AST.
"""

from typing import Dict, List, Any
import uuid


def empty_csf(source_path: str) -> Dict[str, Any]:
    """
    Create an empty CSF structure.
    
    Args:
        source_path: Path to the source file
        
    Returns:
        Empty CSF dict with initialized fields
    """
    return {
        "version": "0.1.0",
        "source_path": source_path,
        "nodes": {},
        "root_ids": [],
        "chunks": [],
    }


def make_node(node_id: str, kind: str, label: str, source_ref: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a CSF node.
    
    Args:
        node_id: Unique identifier for the node
        kind: Node type (function/class/block/statement/module/chunk)
        label: Human-readable name
        source_ref: Source code location reference
        
    Returns:
        CSF node dict
    """
    return {
        "id": node_id,
        "kind": kind,
        "label": label,
        "source_ref": source_ref,
        "children": [],
        "dependencies": [],
        "mutations": [],
        "mutation_affects": [],
        "expansion_state": "collapsed",
        "meta": {},
    }


def generate_node_id() -> str:
    """
    Generate a unique node ID.
    
    Returns:
        Unique string identifier
    """
    return str(uuid.uuid4())


def make_chunk(chunk_id: str, node_ids: List[str], label: str, pressure_score: float = 0.0) -> Dict[str, Any]:
    """
    Create a chunk for working set.
    
    Args:
        chunk_id: Unique identifier for the chunk
        node_ids: List of node IDs belonging to this chunk
        label: Human-readable label
        pressure_score: Recognition Matrix score
        
    Returns:
        Chunk dict
    """
    return {
        "id": chunk_id,
        "node_ids": node_ids,
        "label": label,
        "pressure_score": pressure_score,
    }


# Valid kind values
VALID_KINDS = ["function", "class", "block", "statement", "module", "chunk"]

# Valid expansion states
VALID_EXPANSION_STATES = ["collapsed", "expanded", "inline_preview"]
