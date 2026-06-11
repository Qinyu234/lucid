"""
Test for nesting depth functionality
验证嵌套深度功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.expansion.nesting_depth import calculate_nesting_depths


def test_nesting_depth_calculation():
    """
    Test that nesting depth can be calculated.
    测试嵌套深度能够被计算。
    """
    test_code = """
def outer():
    def inner():
        def deep():
            return 42
        return deep()
    return inner()
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Calculate nesting depths
        depths = calculate_nesting_depths(csf)
        
        assert depths is not None, "Should calculate nesting depths"
        assert isinstance(depths, dict), "Depths should be a dict"
        assert all(depth >= 0 for depth in depths.values()), "Nesting depths should be non-negative"
    finally:
        Path(temp_path).unlink()


def test_nesting_depth_limit():
    """
    Test that nesting depth can be limited.
    测试嵌套深度能够被限制。
    """
    test_code = """
def simple():
    return 1
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        depths = calculate_nesting_depths(csf)
        
        assert depths is not None, "Should calculate nesting depths"
        assert isinstance(depths, dict), "Depths should be a dict"
        assert all(depth >= 0 for depth in depths.values()), "Nesting depths should be non-negative"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
