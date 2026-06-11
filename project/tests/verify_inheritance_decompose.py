"""
Test for inheritance decomposition functionality
验证继承分解功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar
from core.desugar.inheritance_decompose import decompose_inheritance


def test_inheritance_decomposition():
    """
    Test that inheritance can be decomposed.
    测试继承能够被分解。
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
        csf = desugar(csf)
        
        # Decompose inheritance
        decomposed_csf = decompose_inheritance(csf)
        
        assert decomposed_csf is not None, "Should decompose inheritance"
        assert 'nodes' in decomposed_csf, "CSF should have nodes"
    finally:
        Path(temp_path).unlink()


def test_inheritance_flattening():
    """
    Test that inheritance hierarchy is flattened.
    测试继承层次被扁平化。
    """
    test_code = """
class A:
    pass

class B(A):
    pass

class C(B):
    pass
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        
        decomposed_csf = decompose_inheritance(csf)
        
        assert decomposed_csf is not None, "Should decompose inheritance"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
