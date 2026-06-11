"""
Test for complexity estimation functionality
验证复杂度估算功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar
from core.complexity import visualize_complexity


def test_complexity_estimation():
    """
    Test that complexity is estimated.
    测试复杂度能够被估算。
    """
    test_code = """
def simple_function(x):
    return x + 1

def complex_function(data):
    result = []
    for item in data:
        if item > 0:
            for i in range(10):
                result.append(item * i)
    return result
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        
        # Generate test suite first (required for complexity visualization)
        from core.flow import analyze_flows
        from core.testing import generate_test_suite
        csf = analyze_flows(csf)
        test_suite = generate_test_suite(csf)
        
        csf = visualize_complexity(csf, test_suite)
        
        # Check that complexity is estimated
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                # Check for complexity_score (the actual complexity value)
                assert 'complexity_score' in node['meta'], "Should have complexity_score metadata"
                assert node['meta']['complexity_score'] >= 0, "Complexity score should be non-negative"
    finally:
        Path(temp_path).unlink()


def test_complexity_coloring():
    """
    Test that complexity colors are assigned.
    测试复杂度颜色能够被分配。
    """
    test_code = """
def test_func():
    pass
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        
        from core.flow import analyze_flows
        from core.testing import generate_test_suite
        csf = analyze_flows(csf)
        test_suite = generate_test_suite(csf)
        
        csf = visualize_complexity(csf, test_suite)
        
        # Check that color indicators are assigned
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                # Should have color indicator based on test tightness and operational complexity
                assert 'color_indicator' in node['meta'], "Should have color_indicator"
                assert node['meta']['color_indicator'] in ['green', 'yellow', 'red'], \
                    "Color indicator should be green, yellow, or red"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
