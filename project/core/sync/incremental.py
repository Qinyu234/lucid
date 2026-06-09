"""
Incremental CSF Update
Incrementally update CSF when source code changes, preserving expansion_state
"""

import ast
from typing import Dict, Any
from core.csf.schema import empty_csf
from core.sync.visitor import CSFVisitor


def incremental_update(old_csf: Dict[str, Any], new_source: str, source_path: str) -> Dict[str, Any]:
    """
    Incrementally update CSF when source code changes.
    
    Preserves expansion_state for nodes that haven't significantly changed.
    
    Args:
        old_csf: Previous CSF structure
        new_source: New source code
        source_path: Path to the source file
        
    Returns:
        Updated CSF structure
    """
    # Parse new source to get new_csf
    new_csf = parse_from_source(new_source, source_path)
    
    # Match nodes between old and new CSF
    old_nodes = old_csf['nodes']
    new_nodes = new_csf['nodes']
    
    # Build match key: (kind, label, line_start)
    def node_key(node: Dict[str, Any]) -> tuple:
        return (
            node['kind'],
            node['label'],
            node['source_ref']['line_start']
        )
    
    old_keys = {node_id: node_key(node) for node_id, node in old_nodes.items()}
    new_keys = {node_id: node_key(node) for node_id, node in new_nodes.items()}
    
    # Create a mapping from old node to its expansion_state
    old_expansion_states = {}
    for node_id, node in old_nodes.items():
        key = old_keys[node_id]
        old_expansion_states[key] = node['expansion_state']
    
    # Match and preserve expansion_state
    for new_id, new_node in new_nodes.items():
        new_key = new_keys[new_id]
        
        # Find matching old node
        if new_key in old_expansion_states:
            # Match found - preserve expansion_state
            new_node['expansion_state'] = old_expansion_states[new_key]
    
    return new_csf


def parse_from_source(source: str, source_path: str) -> Dict[str, Any]:
    """
    Parse source code string into CSF.
    
    Helper function for incremental_update.
    """
    tree = ast.parse(source, filename=source_path)
    csf = empty_csf(source_path)
    visitor = CSFVisitor(source_path, csf)
    visitor.visit(tree)
    return csf
