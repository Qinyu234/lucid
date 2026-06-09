"""
Inheritance Placeholder
Adds placeholder node for unresolved inheritance
"""

from typing import Dict, Any
from core.csf.schema import generate_node_id


def add_inheritance_placeholder(
    csf: Dict[str, Any],
    child_node: Dict[str, Any],
    parent_name: str
) -> None:
    """
    Add placeholder node for unresolved inheritance.
    
    Args:
        csf: CSF dict to modify
        child_node: Child class CSF node
        parent_name: Name of parent class (not in same file)
    """
    placeholder_id = generate_node_id()
    placeholder_node = {
        'id': placeholder_id,
        'kind': 'statement',
        'label': f'inherited: {parent_name}',
        'source_ref': child_node['source_ref'],
        'children': [],
        'dependencies': [],
        'mutations': [],
        'mutation_affects': [],
        'expansion_state': 'collapsed',
        'meta': {
            'unresolved_inheritance': True,
            'virtual': True,
        },
    }
    
    csf['nodes'][placeholder_id] = placeholder_node
    child_node['children'].append(placeholder_id)
