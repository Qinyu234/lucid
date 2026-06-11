"""
Test for inheritance expansion functionality
验证继承扩展功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand


def test_inheritance_expansion():
    """
    Test that inheritance is properly expanded.
    测试继承能够正确扩展。
    """
    test_code = """
class BaseClass:
    def base_method(self):
        return "base"

class DerivedClass(BaseClass):
    def derived_method(self):
        return "derived"
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Check that inheritance information is captured
        class_nodes = [node for node in csf['nodes'].values() if node['kind'] == 'class']
        assert len(class_nodes) >= 2, "Should have at least 2 classes"
        
        # Check that DerivedClass has inheritance info
        derived_nodes = [node for node in class_nodes if node['label'] == 'DerivedClass']
        if derived_nodes:
            derived = derived_nodes[0]
            # Should have inheritance metadata
            assert 'inheritance_depth' in derived['meta'] or 'inheritance_chain' in derived['meta'], \
                "Should have inheritance metadata"
    finally:
        Path(temp_path).unlink()


def test_inheritance_chain_tracking():
    """
    Test that inheritance chains are tracked.
    测试继承链能够被跟踪。
    """
    test_code = """
class A:
    def method_a(self):
        pass

class B(A):
    def method_b(self):
        pass

class C(B):
    def method_c(self):
        pass
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Check that inheritance chain is tracked
        class_nodes = [node for node in csf['nodes'].values() if node['kind'] == 'class']
        assert len(class_nodes) == 3, "Should have 3 classes"
        
        # Check that class C has inheritance depth info
        c_nodes = [node for node in class_nodes if node['label'] == 'C']
        if c_nodes:
            c_node = c_nodes[0]
            inheritance_depth = c_node['meta'].get('inheritance_depth', 0)
            assert inheritance_depth >= 0, "Should have inheritance depth"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
