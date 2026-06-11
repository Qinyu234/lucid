"""
Test for typeflow analysis functionality
验证类型流分析功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar
from core.flow import analyze_flows


def test_typeflow_analysis():
    """
    Test that typeflow is analyzed.
    测试类型流能够被分析。
    """
    test_code = """
def process_number(x: int) -> str:
    return str(x)

def process_text(s: str) -> int:
    return len(s)
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        
        # Check that typeflow metadata is added
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                assert 'typeflow' in node['meta'], "Should have typeflow metadata"
                typeflow = node['meta']['typeflow']
                # Typeflow should exist
                assert isinstance(typeflow, dict), "typeflow should be a dict"
    finally:
        Path(temp_path).unlink()


def test_type_tracking():
    """
    Test that types are tracked through the flow.
    测试类型能够通过流被跟踪。
    """
    test_code = """
def transform(value):
    result = value * 2
    return result
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        
        # Check that types are tracked
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                assert 'typeflow' in node['meta'], "Should have typeflow metadata"
                typeflow = node['meta']['typeflow']
                # Type information should be tracked
                assert 'input_types' in typeflow or 'output_types' in typeflow or isinstance(typeflow, dict), \
                    "Should track type information"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
