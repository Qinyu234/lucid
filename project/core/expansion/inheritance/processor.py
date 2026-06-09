"""
Inheritance Processor
Processes class nodes and adds inherited methods.
"""

import ast
from typing import Dict, Any
from core.expansion.inheritance_methods import add_inherited_methods
from core.expansion.inheritance_placeholder import add_inheritance_placeholder


def process_class_inheritance(csf_expanded, node, class_ast, class_csf_map):
    """Process inheritance for a single class node."""
    for base in class_ast.bases:
        parent_name = None
        
        if isinstance(base, ast.Name):
            parent_name = base.id
        elif isinstance(base, ast.Attribute):
            parent_name = base.attr
        
        if not parent_name:
            continue
        
        if parent_name in class_csf_map:
            parent_node = class_csf_map[parent_name]
            add_inherited_methods(csf_expanded, parent_node, node, parent_name)
        else:
            add_inheritance_placeholder(csf_expanded, node, parent_name)
