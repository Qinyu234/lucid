"""
Complexity Visualization
Estimates complexity and provides green/red color mapping based on test coverage and operational complexity.
"""

from typing import Dict, Any
from core.complexity.complexity_estimator import estimate_complexity
from core.complexity.color_mapper import get_color_indicator


def visualize_complexity(csf: Dict[str, Any], test_suite: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Calculate complexity and add color indicators to CSF nodes based on test coverage.
    
    Args:
        csf: Input CSF structure
        test_suite: Test suite with coverage information (required for color calculation)
        
    Returns:
        CSF with complexity scores and color indicators added to nodes
    """
    # Estimate complexity for each node
    complexity_scores = estimate_complexity(csf)
    
    # Calculate test tightness and operational complexity for color mapping
    test_metrics = calculate_test_metrics(csf, test_suite)
    
    # Add color indicators to nodes
    for node_id, node in csf['nodes'].items():
        complexity = complexity_scores.get(node_id, 0.5)
        test_tightness = test_metrics.get(node_id, {}).get('tightness', 0.0)
        operational_complexity = test_metrics.get(node_id, {}).get('operational_complexity', complexity)
        
        node['meta']['complexity_score'] = complexity
        node['meta']['test_tightness'] = test_tightness
        node['meta']['operational_complexity'] = operational_complexity
        node['meta']['color_indicator'] = get_color_indicator(test_tightness, operational_complexity)
    
    return csf


def calculate_test_metrics(csf: Dict[str, Any], test_suite: Dict[str, Any] = None) -> Dict[str, Dict[str, float]]:
    """
    Calculate test tightness and operational complexity for each node.
    
    Args:
        csf: Input CSF structure
        test_suite: Test suite with coverage information
        
    Returns:
        Dictionary mapping node_id to test metrics
    """
    test_metrics = {}
    
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            # Calculate test tightness based on test coverage
            tightness = calculate_test_tightness(node, test_suite)
            
            # Calculate operational complexity based on mutations and state changes
            operational_complexity = calculate_operational_complexity(node)
            
            test_metrics[node_id] = {
                'tightness': tightness,
                'operational_complexity': operational_complexity
            }
        else:
            test_metrics[node_id] = {
                'tightness': 0.5,
                'operational_complexity': 0.5
            }
    
    return test_metrics


def calculate_test_tightness(node: Dict[str, Any], test_suite: Dict[str, Any] = None) -> float:
    """
    Calculate test tightness score for a node.
    Higher tightness means better test coverage (0.0 to 1.0).
    
    Args:
        node: CSF node
        test_suite: Test suite with coverage information
        
    Returns:
        Test tightness score (0.0 to 1.0)
    """
    if test_suite is None:
        return 0.0  # No tests = no tightness
    
    # Count tests for this function
    function_id = node['id']
    test_count = 0
    
    # Count unit tests
    for test in test_suite.get('unit_tests', []):
        if test.get('function_id') == function_id:
            test_count += 1
    
    # Count state transition tests
    for test in test_suite.get('state_transition_tests', []):
        if test.get('function_id') == function_id:
            test_count += 1
    
    # Count edge case tests
    for test in test_suite.get('edge_case_tests', []):
        if test.get('function_id') == function_id:
            test_count += 1
    
    # Calculate tightness based on test count and complexity
    complexity = node['meta'].get('complexity_score', 0.5)
    
    # Higher complexity requires more tests for same tightness
    required_tests = int(complexity * 10) + 1  # At least 1 test
    
    if required_tests == 0:
        return 1.0 if test_count > 0 else 0.0
    
    tightness = min(test_count / required_tests, 1.0)
    return tightness


def calculate_operational_complexity(node: Dict[str, Any]) -> float:
    """
    Calculate operational complexity based on mutations and state changes.
    
    Args:
        node: CSF node
        
    Returns:
        Operational complexity score (0.0 to 1.0)
    """
    complexity = 0.0
    
    # Factor 1: Number of mutations
    mutation_count = len(node.get('mutations', []))
    complexity += min(mutation_count / 10.0, 0.4)
    
    # Factor 2: State complexity
    state_complexity = node['meta'].get('state_complexity', 0.0)
    complexity += state_complexity * 0.3
    
    # Factor 3: Data dependencies
    dataflow = node['meta'].get('dataflow', {})
    data_deps = len(dataflow.get('data_dependencies', []))
    complexity += min(data_deps / 10.0, 0.3)
    
    return min(complexity, 1.0)


__all__ = ['visualize_complexity', 'estimate_complexity', 'calculate_test_metrics']
