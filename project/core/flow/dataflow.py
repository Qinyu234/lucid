"""
Dataflow Analysis
Analyzes data flow through the code to understand data propagation.
"""

from typing import Dict, Any, List, Set


def analyze_dataflow(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze data flow through the CSF.
    
    Args:
        csf: Input CSF structure
        
    Returns:
        CSF with dataflow metadata added to nodes
    """
    # Build data dependency graph
    data_graph = build_data_graph(csf)
    
    # Calculate data propagation
    data_propagation = calculate_data_propagation(data_graph)
    
    # Add dataflow metadata to nodes
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            variables = extract_variables(node)
            node['meta']['dataflow'] = {
                'data_inputs': extract_data_inputs(node),
                'data_outputs': extract_data_outputs(node),
                'data_dependencies': data_propagation.get(node_id, []),
                'data_complexity': calculate_data_complexity(node),
                'variables': variables,
                'flow': {
                    'settings': {
                        'track_propagation': True,
                        'detect_cycles': True,
                        'max_depth': 10
                    },
                    'complexity_threshold': 0.7
                },
                'settings': {
                    'track_propagation': True,
                    'detect_cycles': True,
                    'max_depth': 10
                }
            }
    
    return csf


def build_data_graph(csf: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Build a graph of data dependencies between nodes.
    
    Args:
        csf: Input CSF structure
        
    Returns:
        Dictionary mapping node_id to list of node_ids it depends on for data
    """
    data_graph = {}
    
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            # Data dependencies come from function dependencies
            data_dependencies = []
            for dep_id in node.get('dependencies', []):
                dep_node = csf['nodes'].get(dep_id)
                if dep_node:
                    data_dependencies.append(dep_id)
            data_graph[node_id] = data_dependencies
    
    return data_graph


def calculate_data_propagation(data_graph: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Calculate data propagation paths through the graph.
    
    Args:
        data_graph: Data dependency graph
        
    Returns:
        Dictionary mapping node_id to list of all transitive data dependencies
    """
    propagation = {}
    
    for node_id in data_graph:
        visited = set()
        propagation[node_id] = get_transitive_dependencies(data_graph, node_id, visited)
    
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


def extract_data_inputs(node: Dict[str, Any]) -> List[str]:
    """
    Extract data inputs from a function node.
    
    Args:
        node: Function node
        
    Returns:
        List of data input names
    """
    # Placeholder implementation
    # In a real implementation, this would parse the function signature
    return ['*args', '**kwargs']  # Default for now


def extract_data_outputs(node: Dict[str, Any]) -> List[str]:
    """
    Extract data outputs from a function node.
    
    Args:
        node: Function node
        
    Returns:
        List of data output names
    """
    # Placeholder implementation
    # In a real implementation, this would analyze return statements
    return ['return_value']  # Default for now


def calculate_data_complexity(node: Dict[str, Any]) -> float:
    """
    Calculate data complexity for a function.
    
    Args:
        node: Function node
        
    Returns:
        Data complexity score (0.0 to 1.0)
    """
    # Simple metric based on number of dependencies
    dep_count = len(node.get('dependencies', []))
    return min(dep_count / 10.0, 1.0)


def extract_variables(node: Dict[str, Any]) -> List[str]:
    """
    Extract variable names from a function node.
    
    Args:
        node: Function node
        
    Returns:
        List of variable names
    """
    variables = []
    
    # Extract from dependencies
    for dep in node.get('dependencies', []):
        if dep not in variables:
            variables.append(dep)
    
    # Extract from mutations
    for mutation in node.get('mutations', []):
        if mutation not in variables:
            variables.append(mutation)
    
    return variables


__all__ = ['analyze_dataflow']
