"""
Dependency Graph Building and Span Calculation
"""
from typing import Dict, List, Set, Any
from collections import deque


def build_dependency_graph(
    csf: Dict[str, Any],
    function_name_to_ids: Dict[str, List[str]]
) -> Dict[str, Set[str]]:
    """
    Build a dependency graph mapping function node IDs to their dependencies.
    
    Args:
        csf: CSF dict
        function_name_to_ids: Map of function name to node IDs
        
    Returns:
        Dependency graph: node_id -> set of dependent node IDs
    """
    graph: Dict[str, Set[str]] = {}
    
    for node_id, node in csf['nodes'].items():
        if node['kind'] != 'function':
            continue
        
        graph[node_id] = set()
        
        for dep_name in node['dependencies']:
            if dep_name in function_name_to_ids:
                for dep_id in function_name_to_ids[dep_name]:
                    graph[node_id].add(dep_id)
    
    return graph


def calculate_dependency_span(
    start_node_id: str,
    dep_name: str,
    dependency_graph: Dict[str, Set[str]],
    function_name_to_ids: Dict[str, List[str]],
    max_depth: int = 10
) -> int:
    """
    Calculate the dependency chain depth (span) for a given dependency.
    
    Args:
        start_node_id: Starting function node ID
        dep_name: Name of the dependency
        dependency_graph: Dependency graph
        function_name_to_ids: Map of function name to node IDs
        max_depth: Maximum depth to search (to prevent infinite loops)
        
    Returns:
        Dependency chain depth (span)
    """
    if dep_name not in function_name_to_ids:
        return 1  # External dependency, count as 1
    
    # BFS to find shortest path to any node with this name
    queue = deque([(start_node_id, 0)])
    visited: Set[str] = {start_node_id}
    
    while queue:
        current_id, depth = queue.popleft()
        
        if depth > max_depth:
            return max_depth
        
        # Check if current node matches the dependency name
        current_node_id = current_id
        # Get node name from function_name_to_ids (reverse lookup)
        for name, ids in function_name_to_ids.items():
            if current_node_id in ids and name == dep_name:
                return depth
        
        # Add dependencies to queue
        if current_id in dependency_graph:
            for dep_id in dependency_graph[current_id]:
                if dep_id not in visited:
                    visited.add(dep_id)
                    queue.append((dep_id, depth + 1))
    
    return 1  # Default to 1 if not found
