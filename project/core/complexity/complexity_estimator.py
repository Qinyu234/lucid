"""
Complexity Estimator
Estimates complexity scores for CSF nodes based on various metrics.
"""

from typing import Dict, Any, List


def estimate_complexity(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Estimate complexity score for each node in the CSF and add metadata.
    
    Args:
        csf: Input CSF structure
        
    Returns:
        CSF structure with complexity metadata added to nodes
    """
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            # Calculate complexity based on multiple factors
            complexity = calculate_function_complexity(node, csf)
            node['meta']['complexity_score'] = complexity
            
            # Calculate reliability score (inverse of complexity)
            reliability = 1.0 - complexity
            node['meta']['reliability_score'] = reliability
            
            # Calculate readability score (based on complexity and structure)
            readability = calculate_readability_score(node, csf)
            node['meta']['readability_score'] = readability
            
            # Calculate semantic complexity
            semantic_complexity = calculate_semantic_complexity(node, csf)
            node['meta']['semantic_complexity'] = semantic_complexity
        elif node['kind'] == 'class':
            complexity = calculate_class_complexity(node, csf)
            node['meta']['complexity_score'] = complexity
            node['meta']['reliability_score'] = 1.0 - complexity
            node['meta']['readability_score'] = 0.7  # Default for classes
            node['meta']['semantic_complexity'] = complexity * 0.8
        else:
            node['meta']['complexity_score'] = 0.5
            node['meta']['reliability_score'] = 0.5
            node['meta']['readability_score'] = 0.5
            node['meta']['semantic_complexity'] = 0.5
    
    return csf


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


def calculate_readability_score(node: Dict[str, Any], csf: Dict[str, Any]) -> float:
    """
    Calculate readability score for a function node.
    
    Args:
        node: Function node
        csf: CSF structure
        
    Returns:
        Readability score (0.0 to 1.0, higher is more readable)
    """
    readability = 1.0
    
    # Factor 1: Reduce readability based on nesting depth
    child_count = len(node.get('children', []))
    readability -= min(child_count / 20.0, 0.3)
    
    # Factor 2: Reduce readability based on dependencies
    dep_count = len(node.get('dependencies', []))
    readability -= min(dep_count / 15.0, 0.2)
    
    # Factor 3: Reduce readability based on mutations
    mutation_count = len(node.get('mutations', []))
    readability -= min(mutation_count / 10.0, 0.2)
    
    return max(readability, 0.0)


def calculate_semantic_complexity(node: Dict[str, Any], csf: Dict[str, Any]) -> float:
    """
    Calculate semantic complexity for a function node.
    
    Args:
        node: Function node
        csf: CSF structure
        
    Returns:
        Semantic complexity score (0.0 to 1.0, higher is more complex)
    """
    semantic_complexity = 0.0
    
    # Factor 1: Based on dataflow complexity
    if 'dataflow' in node['meta']:
        dataflow = node['meta']['dataflow']
        variable_count = len(dataflow.get('variables', []))
        semantic_complexity += min(variable_count / 10.0, 0.3)
    
    # Factor 2: Based on stateflow complexity
    if 'stateflow' in node['meta']:
        stateflow = node['meta']['stateflow']
        state_count = len(stateflow.get('states', []))
        semantic_complexity += min(state_count / 5.0, 0.3)
    
    # Factor 3: Based on control flow complexity
    child_count = len(node.get('children', []))
    semantic_complexity += min(child_count / 15.0, 0.2)
    
    # Factor 4: Based on operation complexity
    dep_count = len(node.get('dependencies', []))
    semantic_complexity += min(dep_count / 10.0, 0.2)
    
    return min(semantic_complexity, 1.0)


__all__ = ['estimate_complexity']
