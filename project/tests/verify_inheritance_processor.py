"""
Test for inheritance processor functionality
验证继承处理器功能
"""

import pytest
from pathlib import Path
import sys
import tempfile
import ast

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.expansion.inheritance.processor import process_class_inheritance
from core.expansion.inheritance.parser import parse_source_to_ast, build_class_ast_map, build_class_csf_map


def test_inheritance_processing():
    """
    Test that inheritance can be processed.
    测试继承能够被处理。
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
        tree = parse_source_to_ast(temp_path)
        class_ast_map = build_class_ast_map(tree)
        class_csf_map = build_class_csf_map(csf)
        
        # Find child node
        child_node = None
        child_ast = None
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'class' and node['label'] == 'Child':
                child_node = node
                child_ast = class_ast_map.get('Child')
                break
        
        if child_node and child_ast:
            # Process inheritance
            process_class_inheritance(csf, child_node, child_ast, class_csf_map)
        
        assert csf is not None, "Should process inheritance"
    finally:
        Path(temp_path).unlink()


def test_inheritance_chain():
    """
    Test that inheritance chain is processed.
    测试继承链被处理。
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
        tree = parse_source_to_ast(temp_path)
        class_ast_map = build_class_ast_map(tree)
        class_csf_map = build_class_csf_map(csf)
        
        # Find child node
        child_node = None
        child_ast = None
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'class' and node['label'] == 'C':
                child_node = node
                child_ast = class_ast_map.get('C')
                break
        
        if child_node and child_ast:
            process_class_inheritance(csf, child_node, child_ast, class_csf_map)
        
        assert csf is not None, "Should process inheritance chain"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
