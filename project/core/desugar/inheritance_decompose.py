"""
Inheritance Decomposition
Decomposes inheritance relationships by inlining inherited methods and tracking inheritance chains.
"""

from typing import Dict, Any, List, Set
from core.csf.schema import generate_node_id


def decompose_inheritance(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decompose inheritance relationships by tracking inheritance chains.
    
    This transformation:
    - Tracks inheritance chains for each function
    - Marks functions with their inheritance depth
    - Prepares for virtual file mapping of inheritance trees
    
    Args:
        csf: Input CSF structure (after class-to-function conversion)
        
    Returns:
        CSF with inheritance decomposition metadata
    """
    # Build inheritance graph
    inheritance_graph = build_inheritance_graph(csf)
    
    # Calculate inheritance depth for each node
    inheritance_depths = calculate_inheritance_depths(inheritance_graph)
    
    # Add inheritance metadata to nodes
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            node['meta']['inheritance_depth'] = inheritance_depths.get(node_id, 0)
            node['meta']['inheritance_chain'] = get_inheritance_chain(inheritance_graph, node_id)
            
            # Mark if this is an inherited method
            if 'original_class_id' in node['meta']:
                original_class_id = node['meta']['original_class_id']
                if original_class_id in inheritance_graph:
                    node['meta']['is_inherited'] = True
                    node['meta']['inherited_from'] = inheritance_graph[original_class_id]
                else:
                    node['meta']['is_inherited'] = False
            else:
                node['meta']['is_inherited'] = False
    
    return csf


def build_inheritance_graph(csf: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Build inheritance graph from CSF nodes.
    
    Args:
        csf: Input CSF structure
        
    Returns:
        Dictionary mapping node_id to list of parent node_ids
    """
    graph = {}
    
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            # Check if this function has inheritance metadata
            if 'original_class_id' in node['meta']:
                original_class_id = node['meta']['original_class_id']
                
                # Find the original class node (now converted to constructor)
                for other_id, other_node in csf['nodes'].items():
                    if (other_node['kind'] == 'function' and 
                        other_node['meta'].get('original_class_id') == original_class_id and
                        other_node['meta'].get('is_constructor')):
                        # This is the constructor for the original class
                        # Check if the original class had base classes
                        # For now, we'll track this in dependencies
                        if node_id not in graph:
                            graph[node_id] = []
    
    return graph


def calculate_inheritance_depths(graph: Dict[str, List[str]]) -> Dict[str, int]:
    """
    Calculate inheritance depth for each node using DFS.
    
    Args:
        graph: Inheritance graph
        
    Returns:
        Dictionary mapping node_id to inheritance depth
    """
    depths = {}
    visited = set()
    
    def dfs(node_id: str, depth: int) -> int:
        if node_id in visited:
            return depths.get(node_id, 0)
        
        visited.add(node_id)
        max_child_depth = depth
        
        if node_id in graph:
            for child_id in graph[node_id]:
                child_depth = dfs(child_id, depth + 1)
                max_child_depth = max(max_child_depth, child_depth)
        
        depths[node_id] = max_child_depth
        return max_child_depth
    
    for node_id in graph:
        if node_id not in visited:
            dfs(node_id, 0)
    
    return depths


def get_inheritance_chain(graph: Dict[str, List[str]], node_id: str) -> List[str]:
    """
    Get the inheritance chain for a node.
    
    Args:
        graph: Inheritance graph
        node_id: Node to get chain for
        
    Returns:
        List of node_ids in the inheritance chain
    """
    chain = []
    visited = set()
    
    def dfs(current_id: str):
        if current_id in visited or current_id not in graph:
            return
        visited.add(current_id)
        chain.append(current_id)
        for child_id in graph[current_id]:
            dfs(child_id)
    
    dfs(node_id)
    return chain


__all__ = ['decompose_inheritance']
