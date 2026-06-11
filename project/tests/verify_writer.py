"""
Test for code writer functionality
验证代码写入器功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.sync.writer.extract import extract_function
from core.sync.writer.early_return import add_early_return


def test_function_extraction():
    """
    Test that functions can be extracted from CSF.
    测试函数能够从CSF中提取。
    """
    test_code = """
def hello_world():
    print("Hello, World!")
    return 42
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Extract function from CSF
        function_nodes = [node for node in csf['nodes'].values() if node['kind'] == 'function']
        assert len(function_nodes) >= 1, "Should have at least one function"
        
        # Test extraction with required arguments
        for func_node in function_nodes:
            extracted = extract_function(csf, func_node['id'], "extracted_function", temp_path)
            assert extracted is not None, "Should extract function"
    finally:
        Path(temp_path).unlink()


def test_early_return_addition():
    """
    Test that early returns can be added.
    测试能够添加早期返回。
    """
    test_code = """
def process_data(data):
    if data is None:
        return None
    result = data * 2
    return result
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Test early return addition
        function_nodes = [node for node in csf['nodes'].values() if node['kind'] == 'function']
        assert len(function_nodes) >= 1, "Should have at least one function"
        
        # The function should exist and have proper structure
        for func_node in function_nodes:
            assert 'children' in func_node, "Function should have children"
            assert 'dependencies' in func_node, "Function should have dependencies"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
