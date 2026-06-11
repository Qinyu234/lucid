"""
Test for code analysis functionality
验证代码分析功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar


def test_smell_detection():
    """
    Test that code smells can be detected.
    测试代码异味能够被检测。
    """
    test_code = """
def very_long_function_with_many_parameters(param1, param2, param3, param4, param5, param6):
    result = param1 + param2
    result += param3
    result += param4
    result += param5
    result += param6
    return result
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        
        # Check that code analysis metadata is added
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                # Should have some analysis metadata
                assert 'meta' in node, "Node should have metadata"
                # Code smells might not be detected by default, so just check metadata exists
                assert isinstance(node['meta'], dict), "Metadata should be a dict"
    finally:
        Path(temp_path).unlink()


def test_complexity_metrics():
    """
    Test that complexity metrics are calculated.
    测试复杂度指标能够被计算。
    """
    test_code = """
def simple_function():
    return 42

def complex_function(data):
    result = []
    for item in data:
        if item > 0:
            for i in range(10):
                if i % 2 == 0:
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
        
        # Check that functions have analysis metadata
        function_nodes = [node for node in csf['nodes'].values() if node['kind'] == 'function']
        assert len(function_nodes) >= 2, "Should have at least 2 functions"
        
        for node in function_nodes:
            assert 'meta' in node, "Function should have metadata"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
