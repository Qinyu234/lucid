"""
Test for CSF schema functionality
验证CSF模式功能
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.csf.schema import generate_node_id, make_node


def test_node_id_generation():
    """
    Test that node IDs can be generated.
    测试节点ID能够被生成。
    """
    node_id = generate_node_id()
    assert node_id is not None, "Should generate node ID"
    assert isinstance(node_id, str), "Node ID should be a string"
    assert len(node_id) > 0, "Node ID should not be empty"


def test_node_creation():
    """
    Test that nodes can be created with proper structure.
    测试节点能够以正确的结构被创建。
    """
    node_id = generate_node_id()
    source_ref = {"start_line": 1, "end_line": 10}
    node = make_node(
        node_id,
        "function",
        "test_function",
        source_ref
    )
    
    assert node['id'] == node_id, "Node should have correct ID"
    assert node['kind'] == "function", "Node should have correct kind"
    assert node['label'] == "test_function", "Node should have correct label"
    assert node['source_ref'] == source_ref, "Node should have correct source ref"
    assert 'meta' in node, "Node should have metadata"
    assert 'children' in node, "Node should have children list"
    assert 'dependencies' in node, "Node should have dependencies list"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
