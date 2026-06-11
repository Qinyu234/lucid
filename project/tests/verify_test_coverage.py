"""
Test for test coverage analysis functionality
验证测试覆盖率分析功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar
from core.flow import analyze_flows
from core.testing import generate_test_suite, analyze_coverage


def test_coverage_analysis():
    """
    Test that test coverage can be analyzed.
    测试测试覆盖率能够被分析。
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
        
        # Analyze coverage
        coverage = analyze_coverage(csf, test_suite)
        
        # Check that coverage is calculated
        assert 'coverage_percentage' in coverage, "Should have coverage_percentage"
        assert 'function_coverage' in coverage, "Should have function_coverage"
        assert 'total_functions' in coverage, "Should have total_functions"
        
        # Coverage should be between 0 and 100
        assert 0 <= coverage['coverage_percentage'] <= 100, "Coverage should be between 0 and 100"
    finally:
        Path(temp_path).unlink()


def test_coverage_metrics():
    """
    Test that coverage metrics are accurate.
    测试覆盖率指标是准确的。
    """
    test_code = """
def simple_func():
    return 42
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
        
        coverage = analyze_coverage(csf, test_suite)
        
        # Check coverage metrics
        assert coverage['total_functions'] >= 0, "Total functions should be non-negative"
        assert coverage['tested_functions'] >= 0, "Tested functions should be non-negative"
        assert coverage['tested_functions'] <= coverage['total_functions'], \
            "Tested functions should not exceed total functions"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
