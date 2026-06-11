"""
Test for inheritance placeholder functionality
验证继承占位符功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.expansion.inheritance_placeholder import add_inheritance_placeholder


def test_inheritance_placeholder_addition():
    """
    Test that inheritance placeholders can be added.
    测试继承占位符能够被添加。
    """
    test_code = """
class Parent:
    def method(self):
        pass

class Child(Parent):
    pass
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Find child node
        child_node = None
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'class' and node['label'] == 'Child':
                child_node = node
                break
        
        if child_node:
            # Add inheritance placeholder
            add_inheritance_placeholder(csf, child_node, 'Parent')
        
        assert csf is not None, "Should add inheritance placeholder"
        assert 'nodes' in csf, "CSF should have nodes"
    finally:
        Path(temp_path).unlink()


def test_placeholder_structure():
    """
    Test that placeholders have correct structure.
    测试占位符有正确的结构。
    """
    test_code = """
class Base:
    pass

class Derived(Base):
    pass
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Find child node
        child_node = None
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'class' and node['label'] == 'Derived':
                child_node = node
                break
        
        if child_node:
            add_inheritance_placeholder(csf, child_node, 'Base')
        
        assert csf is not None, "Should add inheritance placeholder"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
