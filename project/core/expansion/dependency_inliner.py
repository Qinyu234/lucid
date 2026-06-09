"""
Dependency Inlining
Inlines dependency functions within their callers
"""
import copy
from typing import Dict, Any
from core.csf.schema import generate_node_id


def inline_dependency(
    csf: Dict[str, Any],
    caller_node: Dict[str, Any],
    dep_node: Dict[str, Any],
    dep_node_id: str
) -> None:
    """
    Inline a dependency function's children into the caller.
    
    Args:
        csf: CSF dict to modify
        caller_node: Caller function node
        dep_node: Dependency function node
        dep_node_id: Dependency function node ID
    """
    # Create virtual nodes for each child of the dependency
    for child_id in dep_node['children']:
        if child_id not in csf['nodes']:
            continue
        
        child_node = csf['nodes'][child_id]
        
        # Create virtual copy
        virtual_id = generate_node_id()
        virtual_node = copy.deepcopy(child_node)
        virtual_node['id'] = virtual_id
        virtual_node['meta']['inlined_from'] = dep_node_id
        virtual_node['meta']['virtual'] = True
        
        # Add to CSF
        csf['nodes'][virtual_id] = virtual_node
        caller_node['children'].append(virtual_id)
