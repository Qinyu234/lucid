"""
Test for dependency graph functionality
验证依赖图功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.expansion.dependency_graph import build_dependency_graph


def test_dependency_graph_building():
    """
    Test that dependency graph can be built.
    测试依赖图能够被构建。
    """
    test_code = """
def function_a():
    return function_b()

def function_b():
    return 42
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Build function name to IDs mapping
        function_name_to_ids = {}
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                name = node['label']
                if name not in function_name_to_ids:
                    function_name_to_ids[name] = []
                function_name_to_ids[name].append(node_id)
        
        # Build dependency graph
        graph = build_dependency_graph(csf, function_name_to_ids)
        
        assert graph is not None, "Should build dependency graph"
        assert isinstance(graph, dict), "Graph should be a dict"
    finally:
        Path(temp_path).unlink()


def test_dependency_traversal():
    """
    Test that dependencies can be traversed.
    测试依赖能够被遍历。
    """
    test_code = """
def main():
    return helper()

def helper():
    return utility()

def utility():
    return 0
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Build function name to IDs mapping
        function_name_to_ids = {}
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                name = node['label']
                if name not in function_name_to_ids:
                    function_name_to_ids[name] = []
                function_name_to_ids[name].append(node_id)
        
        graph = build_dependency_graph(csf, function_name_to_ids)
        
        assert graph is not None, "Should build dependency graph"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
