"""
Test Runner
Executes generated tests and reports results.
"""

from typing import Dict, Any, List
import subprocess
import sys


def run_tests(test_suite: Dict[str, Any], output_dir: str = "tests/generated") -> Dict[str, Any]:
    """
    Run a test suite and report results.
    
    Args:
        test_suite: Test suite dictionary
        output_dir: Directory to write test files
        
    Returns:
        Test results dictionary
    """
    results = {
        'total_tests': 0,
        'passed': 0,
        'failed': 0,
        'errors': 0,
        'test_results': []
    }
    
    # Write test files
    test_files = write_test_files(test_suite, output_dir)
    
    # Run each test file
    for test_file in test_files:
        result = run_test_file(test_file)
        results['test_results'].append(result)
        results['total_tests'] += result['total']
        results['passed'] += result['passed']
        results['failed'] += result['failed']
        results['errors'] += result['errors']
    
    return results


def write_test_files(test_suite: Dict[str, Any], output_dir: str) -> List[str]:
    """
    Write test files from test suite.
    
    Args:
        test_suite: Test suite dictionary
        output_dir: Directory to write test files
        
    Returns:
        List of written test file paths
    """
    test_files = []
    
    # Write unit tests
    if test_suite['unit_tests']:
        unit_test_file = f"{output_dir}/test_unit.py"
        write_unit_test_file(unit_test_file, test_suite['unit_tests'])
        test_files.append(unit_test_file)
    
    # Write integration tests
    if test_suite['integration_tests']:
        integration_test_file = f"{output_dir}/test_integration.py"
        write_integration_test_file(integration_test_file, test_suite['integration_tests'])
        test_files.append(integration_test_file)
    
    # Write state transition tests
    if test_suite['state_transition_tests']:
        state_test_file = f"{output_dir}/test_state.py"
        write_state_test_file(state_test_file, test_suite['state_transition_tests'])
        test_files.append(state_test_file)
    
    # Write edge case tests
    if test_suite['edge_case_tests']:
        edge_test_file = f"{output_dir}/test_edge_cases.py"
        write_edge_case_test_file(edge_test_file, test_suite['edge_case_tests'])
        test_files.append(edge_test_file)
    
    return test_files


def run_test_file(test_file: str) -> Dict[str, Any]:
    """
    Run a single test file using pytest.
    
    Args:
        test_file: Path to test file
        
    Returns:
        Test result dictionary
    """
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', test_file, '-v'],
            capture_output=True,
            text=True
        )
        
        # Parse pytest output (simplified)
        output = result.stdout + result.stderr
        
        return {
            'file': test_file,
            'total': output.count('PASSED') + output.count('FAILED'),
            'passed': output.count('PASSED'),
            'failed': output.count('FAILED'),
            'errors': output.count('ERROR'),
            'output': output
        }
    except Exception as e:
        return {
            'file': test_file,
            'total': 0,
            'passed': 0,
            'failed': 0,
            'errors': 1,
            'output': str(e)
        }


def write_unit_test_file(file_path: str, tests: List[Dict[str, Any]]) -> None:
    """Write unit test file."""
    lines = ['"""Auto-generated unit tests"""', 'import pytest', '']
    
    for test in tests:
        lines.append(f"def {test['name']}():")
        lines.append(f'    """{test["description"]}"""')
        lines.append(f'    # Setup: {test["setup_code"]}')
        lines.append('    pass  # TODO: Implement test')
        lines.append('')
    
    with open(file_path, 'w') as f:
        f.write('\n'.join(lines))


def write_integration_test_file(file_path: str, tests: List[Dict[str, Any]]) -> None:
    """Write integration test file."""
    lines = ['"""Auto-generated integration tests"""', 'import pytest', '']
    
    for test in tests:
        lines.append(f"def {test['name']}():")
        lines.append(f'    """{test["description"]}"""')
        lines.append(f'    # Scenario: {test["test_scenario"]}')
        lines.append('    pass  # TODO: Implement test')
        lines.append('')
    
    with open(file_path, 'w') as f:
        f.write('\n'.join(lines))


def write_state_test_file(file_path: str, tests: List[Dict[str, Any]]) -> None:
    """Write state transition test file."""
    lines = ['"""Auto-generated state transition tests"""', 'import pytest', '']
    
    for test in tests:
        lines.append(f"def {test['name']}():")
        lines.append(f'    """{test["description"]}"""')
        lines.append(f'    # Initial state: {test["initial_state"]}')
        lines.append(f'    # Expected state: {test["expected_state"]}')
        lines.append('    pass  # TODO: Implement test')
        lines.append('')
    
    with open(file_path, 'w') as f:
        f.write('\n'.join(lines))


def write_edge_case_test_file(file_path: str, tests: List[Dict[str, Any]]) -> None:
    """Write edge case test file."""
    lines = ['"""Auto-generated edge case tests"""', 'import pytest', '']
    
    for test in tests:
        lines.append(f"def {test['name']}():")
        lines.append(f'    """{test["description"]}"""')
        lines.append(f'    # Edge cases: {test["edge_cases"]}')
        lines.append(f'    # Boundary conditions: {test["boundary_conditions"]}')
        lines.append('    pass  # TODO: Implement test')
        lines.append('')
    
    with open(file_path, 'w') as f:
        f.write('\n'.join(lines))


__all__ = ['run_tests']
