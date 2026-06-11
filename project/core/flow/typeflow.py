"""
Typeflow Analysis
Analyzes type flow through the code to understand type propagation.
"""

from typing import Dict, Any, List, Set


def analyze_typeflow(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze type flow through the CSF.
    
    Args:
        csf: Input CSF structure
        
    Returns:
        CSF with typeflow metadata added to nodes
    """
    # Build type dependency graph
    type_graph = build_type_graph(csf)
    
    # Calculate type propagation
    type_propagation = calculate_type_propagation(type_graph)
    
    # Add typeflow metadata to nodes
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            node['meta']['typeflow'] = {
                'input_types': extract_input_types(node),
                'output_types': extract_output_types(node),
                'type_dependencies': type_propagation.get(node_id, []),
                'type_complexity': calculate_type_complexity(node)
            }
    
    return csf


def build_type_graph(csf: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Build a graph of type dependencies between nodes.
    
    Args:
        csf: Input CSF structure
        
    Returns:
        Dictionary mapping node_id to list of node_ids it depends on for types
    """
    type_graph = {}
    
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            # Type dependencies come from function dependencies
            type_dependencies = []
            for dep_id in node.get('dependencies', []):
                dep_node = csf['nodes'].get(dep_id)
                if dep_node and dep_node['kind'] == 'function':
                    type_dependencies.append(dep_id)
            type_graph[node_id] = type_dependencies
    
    return type_graph


def calculate_type_propagation(type_graph: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Calculate type propagation paths through the graph.
    
    Args:
        type_graph: Type dependency graph
        
    Returns:
        Dictionary mapping node_id to list of all transitive type dependencies
    """
    propagation = {}
    
    for node_id in type_graph:
        visited = set()
        propagation[node_id] = get_transitive_dependencies(type_graph, node_id, visited)
    
    return propagation


def get_transitive_dependencies(graph: Dict[str, List[str]], node_id: str, visited: Set[str]) -> List[str]:
    """
    Get all transitive dependencies for a node.
    
    Args:
        graph: Dependency graph
        node_id: Starting node
        visited: Set of already visited nodes
        
    Returns:
        List of all transitive dependencies
    """
    if node_id in visited or node_id not in graph:
        return []
    
    visited.add(node_id)
    dependencies = []
    
    for dep_id in graph[node_id]:
        dependencies.append(dep_id)
        dependencies.extend(get_transitive_dependencies(graph, dep_id, visited))
    
    return dependencies


def extract_input_types(node: Dict[str, Any]) -> List[str]:
    """
    Extract input types from a function node.
    
    Args:
        node: Function node
        
    Returns:
        List of input type names
    """
    # Placeholder implementation
    # In a real implementation, this would parse the function signature
    return ['any']  # Default to 'any' for now


def extract_output_types(node: Dict[str, Any]) -> List[str]:
    """
    Extract output types from a function node.
    
    Args:
        node: Function node
        
    Returns:
        List of output type names
    """
    # Placeholder implementation
    # In a real implementation, this would analyze return statements
    return ['any']  # Default to 'any' for now


def calculate_type_complexity(node: Dict[str, Any]) -> float:
    """
    Calculate type complexity for a function.
    
    Args:
        node: Function node
        
    Returns:
        Type complexity score (0.0 to 1.0)
    """
    # Simple metric based on number of dependencies
    dep_count = len(node.get('dependencies', []))
    return min(dep_count / 10.0, 1.0)


__all__ = ['analyze_typeflow']
