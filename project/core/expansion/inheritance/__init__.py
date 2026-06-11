"""
Inheritance Expansion
Expands inheritance relationships by adding virtual inherited nodes to child classes.
"""

import copy
from typing import Dict, Any
from core.expansion.inheritance.parser import parse_source_to_ast, build_class_ast_map, build_class_csf_map
from core.expansion.inheritance.processor import process_class_inheritance


def calculate_inheritance_depth(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate inheritance depth and chain for each class.
    
    Args:
        csf: CSF dict
        
    Returns:
        CSF with inheritance metadata added to class nodes
    """
    # Build inheritance graph
    inheritance_graph = {}
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'class':
            class_name = node['label']
            inheritance_graph[class_name] = []
            
            # Get base classes from AST or metadata
            if 'bases' in node:
                for base in node['bases']:
                    inheritance_graph[class_name].append(base)
    
    # Calculate depth and chains
    def get_inheritance_chain(class_name: str, visited: set = None) -> list:
        if visited is None:
            visited = set()
        if class_name in visited:
            return []
        visited.add(class_name)
        
        chain = [class_name]
        if class_name in inheritance_graph:
            for base in inheritance_graph[class_name]:
                chain.extend(get_inheritance_chain(base, visited))
        return chain
    
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'class':
            class_name = node['label']
            chain = get_inheritance_chain(class_name)
            depth = len(chain) - 1  # depth is number of parents
            
            node['meta']['inheritance_chain'] = chain
            node['meta']['inheritance_depth'] = depth
    
    return csf


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
    
    # Calculate inheritance depth and chains
    csf_expanded = calculate_inheritance_depth(csf_expanded)
    
    return csf_expanded
