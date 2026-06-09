"""
Inheritance Methods Addition
Adds inherited methods from parent class to child as virtual nodes
"""

import copy
from typing import Dict, Any
from core.csf.schema import generate_node_id


def add_inherited_methods(
    csf: Dict[str, Any],
    parent_node: Dict[str, Any],
    child_node: Dict[str, Any],
    parent_name: str
) -> None:
    """
    Add inherited methods from parent class to child as virtual nodes.
    
    Args:
        csf: CSF dict to modify
        parent_node: Parent class CSF node
        child_node: Child class CSF node
        parent_name: Name of parent class
    """
    # Get all method nodes from parent class
    parent_method_ids = parent_node['children']
    
    for method_id in parent_method_ids:
        if method_id not in csf['nodes']:
            continue
        
        method_node = csf['nodes'][method_id]
        if method_node['kind'] != 'function':
            continue
        
        # Create virtual node for inherited method
        virtual_id = generate_node_id()
        virtual_node = copy.deepcopy(method_node)
        virtual_node['id'] = virtual_id
        virtual_node['meta']['inherited_from'] = parent_name
        virtual_node['meta']['virtual'] = True
        
        # Add to CSF
        csf['nodes'][virtual_id] = virtual_node
        child_node['children'].append(virtual_id)
