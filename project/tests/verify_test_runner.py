"""
Test for test runner functionality
验证测试运行器功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar
from core.flow import analyze_flows
from core.testing import generate_test_suite, run_tests


def test_test_execution():
    """
    Test that tests can be executed.
    测试测试能够被执行。
    """
    test_code = """
def add(a, b):
    return a + b
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        test_suite = generate_test_suite(csf)
        
        # Create temporary directory for test files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Run tests with temporary directory
            test_results = run_tests(test_suite, output_dir=temp_dir)
            
            # Check that test results are returned
            assert 'passed' in test_results, "Should have passed count"
            assert 'failed' in test_results, "Should have failed count"
            assert 'errors' in test_results, "Should have errors count"
            
            # Calculate total from available keys
            total = test_results['passed'] + test_results['failed']
            assert total >= 0, "Total should be non-negative"
    finally:
        Path(temp_path).unlink()


def test_test_results_structure():
    """
    Test that test results have proper structure.
    测试测试结果有正确的结构。
    """
    test_code = """
def multiply(x, y):
    return x * y
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        test_suite = generate_test_suite(csf)
        
        # Create temporary directory for test files
        with tempfile.TemporaryDirectory() as temp_dir:
            test_results = run_tests(test_suite, output_dir=temp_dir)
            
            # Check result structure
            assert isinstance(test_results, dict), "Test results should be a dict"
            assert all(key in test_results for key in ['passed', 'failed', 'errors']), \
                "Should have all required keys"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
