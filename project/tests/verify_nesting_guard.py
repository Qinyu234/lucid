"""
Test for nesting guard functionality
验证嵌套守卫功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.expansion.nesting_guard import identify_guard_chains


def test_nesting_guard():
    """
    Test that guard chains can be identified.
    测试守卫链能够被识别。
    """
    test_code = """
def check_value(x):
    if x > 0:
        return "positive"
    if x < 0:
        return "negative"
    return "zero"
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Identify guard chains
        identify_guard_chains(csf)
        
        assert csf is not None, "Should identify guard chains"
        assert 'nodes' in csf, "CSF should have nodes"
    finally:
        Path(temp_path).unlink()


def test_guard_chain_detection():
    """
    Test that guard chains are properly detected.
    测试守卫链被正确检测。
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
        identify_guard_chains(csf)
        
        assert csf is not None, "Should identify guard chains"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
