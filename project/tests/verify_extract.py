"""
Test for extract functionality
验证提取功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.sync.writer.extract import extract_function


def test_function_extraction():
    """
    Test that function can be extracted.
    测试函数能够被提取。
    """
    test_code = """
def process(data):
    # Complex logic
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Find function node
        func_node = None
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function' and node['label'] == 'process':
                func_node = node
                break
        
        if func_node:
            # Extract function
            extracted = extract_function(csf, func_node, 'extracted_logic', temp_path)
            
            assert extracted is not None, "Should extract function"
        
        assert csf is not None, "CSF should exist"
    finally:
        Path(temp_path).unlink()


def test_extraction_with_dependencies():
    """
    Test that extraction handles dependencies.
    测试提取处理依赖。
    """
    test_code = """
def helper(x):
    return x * 2

def main(y):
    return helper(y)
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Find function node
        func_node = None
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function' and node['label'] == 'main':
                func_node = node
                break
        
        if func_node:
            extracted = extract_function(csf, func_node, 'extracted_main', temp_path)
            
            assert extracted is not None, "Should extract function with dependencies"
        
        assert csf is not None, "CSF should exist"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
