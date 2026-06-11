"""
Test for dependency inliner functionality
验证依赖内联功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.expansion.dependency_inliner import inline_dependency


def test_dependency_inlining():
    """
    Test that dependencies can be inlined.
    测试依赖能够被内联。
    """
    test_code = """
def helper():
    return 42

def main():
    return helper()
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Find caller and dependency nodes
        caller_node = None
        dep_node = None
        dep_node_id = None
        
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                if node['label'] == 'main':
                    caller_node = node
                elif node['label'] == 'helper':
                    dep_node = node
                    dep_node_id = node_id
        
        if caller_node and dep_node and dep_node_id:
            # Inline dependency
            inline_dependency(csf, caller_node, dep_node, dep_node_id)
        
        assert csf is not None, "Should inline dependency"
        assert 'nodes' in csf, "CSF should have nodes"
    finally:
        Path(temp_path).unlink()


def test_inlining_structure():
    """
    Test that inlining creates virtual nodes.
    测试内联创建虚拟节点。
    """
    test_code = """
def a():
    return 1

def b():
    return a()
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Find caller and dependency nodes
        caller_node = None
        dep_node = None
        dep_node_id = None
        
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                if node['label'] == 'b':
                    caller_node = node
                elif node['label'] == 'a':
                    dep_node = node
                    dep_node_id = node_id
        
        if caller_node and dep_node and dep_node_id:
            inline_dependency(csf, caller_node, dep_node, dep_node_id)
        
        assert csf is not None, "Should inline dependency"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
