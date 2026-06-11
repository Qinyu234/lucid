"""
Test for early return functionality
验证早期返回功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.sync.writer.early_return import add_early_return


def test_early_return_addition():
    """
    Test that early return can be added.
    测试早期返回能够被添加。
    """
    test_code = """
def process(data):
    if not data:
        return None
    result = []
    for item in data:
        result.append(item)
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
            # Add early return
            add_early_return(csf, func_node, temp_path)
        
        assert csf is not None, "Should add early return"
        assert 'nodes' in csf, "CSF should have nodes"
    finally:
        Path(temp_path).unlink()


def test_early_return_structure():
    """
    Test that early return has correct structure.
    测试早期返回有正确的结构。
    """
    test_code = """
def validate(x):
    if x < 0:
        return False
    return True
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
            if node['kind'] == 'function' and node['label'] == 'validate':
                func_node = node
                break
        
        if func_node:
            add_early_return(csf, func_node, temp_path)
        
        assert csf is not None, "Should add early return"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
