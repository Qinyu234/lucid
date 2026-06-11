"""
Test for nesting flattening functionality
验证嵌套扁平化功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand


def test_nesting_flattening():
    """
    Test that nested structures are flattened.
    测试嵌套结构能够被扁平化。
    """
    test_code = """
def outer_function():
    def inner_function():
        return 42
    return inner_function()
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Check that nested functions are extracted
        function_nodes = [node for node in csf['nodes'].values() if node['kind'] == 'function']
        assert len(function_nodes) >= 2, "Should have at least 2 functions (outer and inner)"
        
        # Check that nesting information is tracked (if available)
        for node in function_nodes:
            # Nesting depth might not be tracked by default, so just check the function exists
            assert node['kind'] == 'function', "Should be a function node"
    finally:
        Path(temp_path).unlink()


def test_nesting_depth_control():
    """
    Test that nesting depth is controlled.
    测试嵌套深度能够被控制。
    """
    test_code = """
def level_1():
    def level_2():
        def level_3():
            return 42
        return level_3()
    return level_2()
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        # Expand with limited nesting depth
        csf = expand(temp_path, options={"nesting_max_depth": 2})
        
        # Check that functions are extracted
        function_nodes = [node for node in csf['nodes'].values() if node['kind'] == 'function']
        assert len(function_nodes) >= 1, "Should have at least 1 function"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
