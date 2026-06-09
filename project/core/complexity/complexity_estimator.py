"""
Complexity Estimator
Estimates complexity scores for CSF nodes based on various metrics.
"""

from typing import Dict, Any, List


def estimate_complexity(csf: Dict[str, Any]) -> Dict[str, float]:
    """
    Estimate complexity score for each node in the CSF.
    
    Args:
        csf: Input CSF structure
        
    Returns:
        Dictionary mapping node_id to complexity score (0.0 to 1.0)
    """
    complexity_scores = {}
    
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            # Calculate complexity based on multiple factors
            complexity = calculate_function_complexity(node, csf)
            complexity_scores[node_id] = complexity
        elif node['kind'] == 'class':
            complexity = calculate_class_complexity(node, csf)
            complexity_scores[node_id] = complexity
        else:
            complexity_scores[node_id] = 0.5  # Default complexity
    
    return complexity_scores


def calculate_function_complexity(node: Dict[str, Any], csf: Dict[str, Any]) -> float:
    """
    Calculate complexity score for a function node.
    
    Args:
        node: Function node
        csf: CSF structure
        
    Returns:
        Complexity score (0.0 to 1.0, higher is more complex)
    """
    complexity = 0.0
    
    # Factor 1: Number of children (nested blocks)
    child_count = len(node.get('children', []))
    complexity += min(child_count / 10.0, 0.3)
    
    # Factor 2: Number of dependencies
    dep_count = len(node.get('dependencies', []))
    complexity += min(dep_count / 10.0, 0.2)
    
    # Factor 3: Number of mutations
    mutation_count = len(node.get('mutations', []))
    complexity += min(mutation_count / 10.0, 0.2)
    
    # Factor 4: State complexity (if available)
    state_complexity = node['meta'].get('state_complexity', 0.0)
    complexity += state_complexity * 0.2
    
    # Factor 5: Inheritance depth (if available)
    inheritance_depth = node['meta'].get('inheritance_depth', 0)
    complexity += min(inheritance_depth / 5.0, 0.1)
    
    return min(complexity, 1.0)


def calculate_class_complexity(node: Dict[str, Any], csf: Dict[str, Any]) -> float:
    """
    Calculate complexity score for a class node.
    
    Args:
        node: Class node
        csf: CSF structure
        
    Returns:
        Complexity score (0.0 to 1.0)
    """
    complexity = 0.0
    
    # Factor 1: Number of methods (children)
    child_count = len(node.get('children', []))
    complexity += min(child_count / 20.0, 0.4)
    
    # Factor 2: Inheritance depth
    inheritance_depth = node['meta'].get('inheritance_depth', 0)
    complexity += min(inheritance_depth / 5.0, 0.3)
    
    # Factor 3: Total complexity of all methods
    method_complexity_sum = 0.0
    for child_id in node.get('children', []):
        child_node = csf['nodes'].get(child_id)
        if child_node:
            method_complexity_sum += calculate_function_complexity(child_node, csf)
    
    avg_method_complexity = method_complexity_sum / max(child_count, 1)
    complexity += avg_method_complexity * 0.3
    
    return min(complexity, 1.0)


__all__ = ['estimate_complexity']
