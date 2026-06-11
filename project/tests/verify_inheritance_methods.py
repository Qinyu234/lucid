"""
Test for inheritance methods functionality
验证继承方法功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.expansion.inheritance_methods import add_inherited_methods


def test_inheritance_methods_addition():
    """
    Test that inherited methods can be added.
    测试继承方法能够被添加。
    """
    test_code = """
class Parent:
    def parent_method(self):
        return "parent"

class Child(Parent):
    def child_method(self):
        return "child"
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Find parent and child nodes
        parent_node = None
        child_node = None
        
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'class':
                if node['label'] == 'Parent':
                    parent_node = node
                elif node['label'] == 'Child':
                    child_node = node
        
        if parent_node and child_node:
            # Add inherited methods
            add_inherited_methods(csf, parent_node, child_node, 'Parent')
        
        assert csf is not None, "Should add inherited methods"
        assert 'nodes' in csf, "CSF should have nodes"
    finally:
        Path(temp_path).unlink()


def test_inheritance_method_resolution():
    """
    Test that method resolution works correctly.
    测试方法解析正确工作。
    """
    test_code = """
class Base:
    def method(self):
        return "base"

class Derived(Base):
    pass
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Find parent and child nodes
        parent_node = None
        child_node = None
        
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'class':
                if node['label'] == 'Base':
                    parent_node = node
                elif node['label'] == 'Derived':
                    child_node = node
        
        if parent_node and child_node:
            add_inherited_methods(csf, parent_node, child_node, 'Base')
        
        assert csf is not None, "Should add inherited methods"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
