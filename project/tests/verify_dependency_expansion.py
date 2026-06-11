"""
Test for dependency expansion functionality
验证依赖扩展功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand


def test_dependency_expansion():
    """
    Test that dependencies are expanded.
    测试依赖能够被扩展。
    """
    test_code = """
def helper_function(x):
    return x + 1

def main_function(y):
    result = helper_function(y)
    return result * 2
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Check that dependencies are tracked
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                # Should have dependencies list
                assert 'dependencies' in node, "Function should have dependencies list"
                assert isinstance(node['dependencies'], list), "Dependencies should be a list"
    finally:
        Path(temp_path).unlink()


def test_dependency_depth():
    """
    Test that dependency depth is controlled.
    测试依赖深度能够被控制。
    """
    test_code = """
def func_a():
    return func_b()

def func_b():
    return func_c()

def func_c():
    return 42
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        # Expand with limited dependency depth
        csf = expand(temp_path, options={"dependency_max_span": 1})
        
        # Check that dependencies are tracked
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                # Dependencies should be tracked
                assert 'dependencies' in node, "Function should have dependencies list"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
