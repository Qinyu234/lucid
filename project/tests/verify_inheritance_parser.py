"""
Test for inheritance parser functionality
验证继承解析器功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion.inheritance.parser import parse_source_to_ast, build_class_ast_map


def test_inheritance_parsing():
    """
    Test that source can be parsed to AST.
    测试源代码能够被解析为AST。
    """
    test_code = """
class Parent:
    pass

class Child(Parent):
    pass
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        # Parse source to AST
        tree = parse_source_to_ast(temp_path)
        
        assert tree is not None, "Should parse source to AST"
        
        # Build class map
        class_map = build_class_ast_map(tree)
        
        assert class_map is not None, "Should build class map"
        assert 'Parent' in class_map, "Should have Parent class"
        assert 'Child' in class_map, "Should have Child class"
    finally:
        Path(temp_path).unlink()


def test_class_map_building():
    """
    Test that class AST map can be built.
    测试类AST映射能够被构建。
    """
    test_code = """
class A:
    pass

class B:
    pass

class C(A, B):
    pass
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        tree = parse_source_to_ast(temp_path)
        class_map = build_class_ast_map(tree)
        
        assert class_map is not None, "Should build class map"
        assert len(class_map) == 3, "Should have 3 classes"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
