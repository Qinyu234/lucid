"""
Inheritance Expansion
Expands inheritance relationships by adding virtual inherited nodes to child classes.
"""

import copy
from typing import Dict, Any
from core.expansion.inheritance.parser import parse_source_to_ast, build_class_ast_map, build_class_csf_map
from core.expansion.inheritance.processor import process_class_inheritance


def expand_inheritance(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Expand inheritance relationships in CSF.
    
    Args:
        csf: CSF dict to expand
        
    Returns:
        Updated CSF dict with virtual inherited nodes (copy, not modifying original)
    """
    csf_expanded = copy.deepcopy(csf)
    
    tree = parse_source_to_ast(csf_expanded['source_path'])
    if not tree:
        return csf_expanded
    
    class_ast_map = build_class_ast_map(tree)
    class_csf_map = build_class_csf_map(csf_expanded)
    
    for node_id, node in list(csf_expanded['nodes'].items()):
        if node['kind'] != 'class':
            continue
        
        class_name = node['label']
        if class_name not in class_ast_map:
            continue
        
        class_ast = class_ast_map[class_name]
        process_class_inheritance(csf_expanded, node, class_ast, class_csf_map)
    
    return csf_expanded
