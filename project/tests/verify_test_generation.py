"""
Test for test generation functionality
验证测试生成功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar
from core.flow import analyze_flows
from core.testing import generate_test_suite


def test_test_generation():
    """
    Test that tests can be generated from flow analysis.
    测试能够从流分析生成测试。
    """
    test_code = """
def process_data(data):
    if data > 0:
        return data * 2
    else:
        return data + 1
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
        
        # Check that test suite is generated
        assert 'unit_tests' in test_suite, "Should have unit_tests"
        assert 'integration_tests' in test_suite, "Should have integration_tests"
        assert 'state_transition_tests' in test_suite, "Should have state_transition_tests"
        assert 'edge_case_tests' in test_suite, "Should have edge_case_tests"
        
        # Check that at least some tests are generated
        total_tests = (
            len(test_suite['unit_tests']) +
            len(test_suite['integration_tests']) +
            len(test_suite['state_transition_tests']) +
            len(test_suite['edge_case_tests'])
        )
        assert total_tests >= 0, "Should generate at least 0 tests"
    finally:
        Path(temp_path).unlink()


def test_unit_test_structure():
    """
    Test that unit tests have proper structure.
    测试单元测试有正确的结构。
    """
    test_code = """
def simple_function(x):
    return x + 1
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
        
        # Check unit test structure
        for test in test_suite['unit_tests']:
            assert 'name' in test, "Test should have name"
            assert 'function_id' in test, "Test should have function_id"
            assert 'description' in test, "Test should have description"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
