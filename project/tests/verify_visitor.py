"""
Test for AST visitor functionality
验证AST访问器功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.sync.visitor import CSFVisitor
from core.csf.schema import empty_csf


def test_visitor_initialization():
    """
    Test that visitor can be initialized.
    测试访问器能够被初始化。
    """
    csf = empty_csf("test_source.py")
    visitor = CSFVisitor("test_source.py", csf)
    assert visitor is not None, "Visitor should be created"
    assert visitor.source_path == "test_source.py", "Visitor should have source path"


def test_visitor_module_visit():
    """
    Test that visitor can visit module nodes.
    测试访问器能够访问模块节点。
    """
    import ast
    
    code = """
def test_function():
    return 42
"""
    
    tree = ast.parse(code)
    csf = empty_csf("test_source.py")
    visitor = CSFVisitor("test_source.py", csf)
    
    visitor.visit(tree)
    
    # Check that nodes were created
    assert len(csf['nodes']) > 0, "Visitor should create nodes"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
