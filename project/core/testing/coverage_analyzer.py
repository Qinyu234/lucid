"""
Coverage Analyzer
Analyzes test coverage and generates coverage reports.
"""

from typing import Dict, Any, List


def analyze_coverage(csf: Dict[str, Any], test_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze test coverage based on CSF and test results.
    
    Args:
        csf: CSF structure
        test_results: Test execution results
        
    Returns:
        Coverage analysis dictionary
    """
    coverage = {
        'total_functions': 0,
        'tested_functions': 0,
        'coverage_percentage': 0.0,
        'untested_functions': [],
        'function_coverage': {}
    }
    
    # Count total functions
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            coverage['total_functions'] += 1
            
            # Check if function has tests
            is_tested = check_function_has_tests(node, test_results)
            if is_tested:
                coverage['tested_functions'] += 1
            else:
                coverage['untested_functions'].append({
                    'id': node_id,
                    'label': node['label'],
                    'complexity': node['meta'].get('complexity_score', 0.0)
                })
            
            coverage['function_coverage'][node_id] = {
                'label': node['label'],
                'tested': is_tested,
                'complexity': node['meta'].get('complexity_score', 0.0),
                'state_mutations': len(node['meta'].get('state_mutations', []))
            }
    
    # Calculate coverage percentage
    if coverage['total_functions'] > 0:
        coverage['coverage_percentage'] = (coverage['tested_functions'] / coverage['total_functions']) * 100
    
    return coverage


def check_function_has_tests(node: Dict[str, Any], test_results: Dict[str, Any]) -> bool:
    """
    Check if a function has corresponding tests.
    
    Args:
        node: Function node
        test_results: Test execution results
        
    Returns:
        True if function has tests, False otherwise
    """
    # Check if test results contain tests for this function
    function_label = node['label']
    
    for result in test_results.get('test_results', []):
        output = result.get('output', '')
        if function_label in output:
            return True
    
    return False


def generate_coverage_report(coverage: Dict[str, Any]) -> str:
    """
    Generate a human-readable coverage report.
    
    Args:
        coverage: Coverage analysis dictionary
        
    Returns:
        Formatted coverage report string
    """
    lines = []
    lines.append("=" * 60)
    lines.append("Test Coverage Report")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Total Functions: {coverage['total_functions']}")
    lines.append(f"Tested Functions: {coverage['tested_functions']}")
    lines.append(f"Coverage: {coverage['coverage_percentage']:.1f}%")
    lines.append("")
    
    if coverage['untested_functions']:
        lines.append("Untested Functions:")
        for func in coverage['untested_functions']:
            lines.append(f"  - {func['label']} (complexity: {func['complexity']:.2f})")
        lines.append("")
    
    lines.append("Function Coverage Details:")
    for node_id, func_cov in coverage['function_coverage'].items():
        status = "✓" if func_cov['tested'] else "✗"
        lines.append(f"  {status} {func_cov['label']} - complexity: {func_cov['complexity']:.2f}, state mutations: {func_cov['state_mutations']}")
    
    lines.append("")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def suggest_coverage_improvements(coverage: Dict[str, Any]) -> List[str]:
    """
    Suggest improvements to increase test coverage.
    
    Args:
        coverage: Coverage analysis dictionary
        
    Returns:
        List of improvement suggestions
    """
    suggestions = []
    
    # Suggest tests for untested high-complexity functions
    high_complexity_untested = [
        func for func in coverage['untested_functions']
        if func['complexity'] > 0.7
    ]
    
    if high_complexity_untested:
        suggestions.append(
            f"Priority: Add tests for {len(high_complexity_untested)} high-complexity untested functions"
        )
        for func in high_complexity_untested[:3]:  # Top 3
            suggestions.append(f"  - {func['label']} (complexity: {func['complexity']:.2f})")
    
    # Suggest state transition tests
    state_mutation_functions = [
        node_id for node_id, func_cov in coverage['function_coverage'].items()
        if func_cov['state_mutations'] > 0 and not func_cov['tested']
    ]
    
    if state_mutation_functions:
        suggestions.append(
            f"Consider: Add state transition tests for {len(state_mutation_functions)} functions with state mutations"
        )
    
    # General suggestions
    if coverage['coverage_percentage'] < 50:
        suggestions.append("Overall: Test coverage is below 50%, consider adding more unit tests")
    elif coverage['coverage_percentage'] < 80:
        suggestions.append("Overall: Test coverage is below 80%, consider adding integration tests")
    
    return suggestions


__all__ = ['analyze_coverage', 'generate_coverage_report', 'suggest_coverage_improvements']
