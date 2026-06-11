"""
Test Generation Module
Automatically generates tests from dataflow and stateflow analysis.
"""

from typing import Dict, Any
from core.testing.test_generator import generate_tests_from_flows
from core.testing.test_runner import run_tests
from core.testing.coverage_analyzer import analyze_coverage


def generate_test_suite(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a complete test suite from CSF flow analysis.
    
    Args:
        csf: Input CSF structure with flow analysis metadata
        
    Returns:
        Dictionary containing generated test suite
    """
    # Generate tests from dataflow and stateflow
    test_suite = generate_tests_from_flows(csf)
    
    return test_suite


__all__ = ['generate_test_suite', 'generate_tests_from_flows', 'run_tests', 'analyze_coverage']
