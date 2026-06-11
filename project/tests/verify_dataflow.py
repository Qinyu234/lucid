"""
Test for dataflow analysis functionality
验证数据流分析功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar
from core.flow import analyze_flows


def test_dataflow_analysis():
    """
    Test that dataflow is analyzed.
    测试数据流能够被分析。
    """
    test_code = """
def process_data(x, y):
    result = x + y
    return result * 2
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        
        # Check that dataflow metadata is added
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                assert 'dataflow' in node['meta'], "Should have dataflow metadata"
                dataflow = node['meta']['dataflow']
                assert 'data_inputs' in dataflow, "Should have data_inputs"
                assert 'data_outputs' in dataflow, "Should have data_outputs"
    finally:
        Path(temp_path).unlink()


def test_data_dependencies():
    """
    Test that data dependencies are tracked.
    测试数据依赖能够被跟踪。
    """
    test_code = """
def calculate(a, b, c):
    x = a + b
    y = x * c
    return y
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        
        # Check that data dependencies are tracked
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                assert 'dataflow' in node['meta'], "Should have dataflow metadata"
                dataflow = node['meta']['dataflow']
                assert 'data_dependencies' in dataflow, "Should have data_dependencies"
                # Dependencies should be a list
                assert isinstance(dataflow['data_dependencies'], list), "data_dependencies should be a list"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
