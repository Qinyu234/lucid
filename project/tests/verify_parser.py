"""
Test for parser functionality
验证解析器功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.sync.parser import parse


def test_parse_python_file():
    """
    Test that Python files can be parsed.
    测试 Python 文件能够被解析。
    """
    test_code = """
def hello_world():
    print("Hello, World!")

class TestClass:
    def method(self):
        return 42
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = parse(temp_path)
        
        # Check that CSF structure is created
        assert 'nodes' in csf, "CSF should have nodes"
        assert 'root_ids' in csf, "CSF should have root_ids"
        assert 'source_path' in csf, "CSF should have source_path"
        
        # Check that nodes are created
        assert len(csf['nodes']) > 0, "Should have at least one node"
        
        # Check for function and class nodes
        function_nodes = [node for node in csf['nodes'].values() if node['kind'] == 'function']
        class_nodes = [node for node in csf['nodes'].values() if node['kind'] == 'class']
        
        assert len(function_nodes) >= 1, "Should have at least one function"
        assert len(class_nodes) >= 1, "Should have at least one class"
    finally:
        Path(temp_path).unlink()


def test_parse_structure():
    """
    Test that parsed structure has correct properties.
    测试解析的结构有正确的属性。
    """
    test_code = """
def simple_func(x, y):
    return x + y
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = parse(temp_path)
        
        # Check node structure
        for node_id, node in csf['nodes'].items():
            assert 'id' in node, "Node should have id"
            assert 'kind' in node, "Node should have kind"
            assert 'label' in node, "Node should have label"
            assert 'meta' in node, "Node should have meta"
            assert 'children' in node, "Node should have children"
            assert 'dependencies' in node, "Node should have dependencies"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
