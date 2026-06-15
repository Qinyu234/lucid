"""
Tests for graph layer
Tests code graph building and node relationships
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.graph.builder import build_code_graph, CodeGraph
from core.graph.nodes import Node, NodeType, create_function_node, create_class_node, create_variable_node


class TestNodeCreation:
    """Test node creation and properties."""
    
    def test_create_function_node(self):
        """Test creation of function node."""
        node = create_function_node("test_func", 10, 5, "test.py")
        
        assert node.name == "test_func"
        assert node.type == NodeType.FUNCTION
        assert node.source_ref['line'] == 10
        assert node.source_ref['column'] == 5
        assert node.source_ref['file_path'] == "test.py"
        assert len(node.writes) == 0
        assert len(node.reads) == 0
        assert len(node.callees) == 0
        assert len(node.callers) == 0
    
    def test_create_class_node(self):
        """Test creation of class node (mapped to MODULE per ARCHITECTURE)."""
        node = create_class_node("TestClass", 5, 0, "test.py", "BaseClass")
        
        assert node.name == "TestClass"
        assert node.type == NodeType.MODULE  # Mapped to MODULE per ARCHITECTURE
        assert node.source_ref['line'] == 5
        assert node.meta['base_class'] == "BaseClass"
    
    def test_create_class_node_without_base(self):
        """Test creation of class node (mapped to MODULE per ARCHITECTURE) without base class."""
        node = create_class_node("TestClass", 5, 0, "test.py")
        
        assert node.name == "TestClass"
        assert node.type == NodeType.MODULE  # Mapped to MODULE per ARCHITECTURE
        assert node.meta.get('base_class') is None
    
    def test_create_variable_node(self):
        """Test creation of variable node (mapped to STATE per ARCHITECTURE)."""
        node = create_variable_node("x", 15, 4, "test.py", "42")
        
        assert node.name == "x"
        assert node.type == NodeType.STATE  # Mapped to STATE per ARCHITECTURE
        assert node.source_ref['line'] == 15
        assert node.meta['initial_value'] == "42"
    
    def test_node_to_dict(self):
        """Test node serialization to dictionary."""
        node = create_function_node("test_func", 10, 5, "test.py")
        node.callees.append("other_func_id")
        
        node_dict = node.to_dict()
        
        assert node_dict['name'] == "test_func"
        assert node_dict['type'] == "function"
        assert node_dict['callees'] == ["other_func_id"]
        assert 'source_ref' in node_dict


class TestCodeGraph:
    """Test CodeGraph functionality."""
    
    def test_graph_initialization(self):
        """Test graph initialization."""
        graph = CodeGraph("test.py")
        
        assert graph.file_path == "test.py"
        assert len(graph.nodes) == 0
        assert len(graph.by_name) == 0
        assert graph.language == ""
    
    def test_add_node(self):
        """Test adding nodes to graph."""
        graph = CodeGraph("test.py")
        node = create_function_node("test_func", 10, 5, "test.py")
        
        graph.add_node(node)
        
        assert len(graph.nodes) == 1
        assert node.id in graph.nodes
        assert "test_func" in graph.by_name
        assert node.id in graph.by_name["test_func"]
    
    def test_add_multiple_nodes_same_name(self):
        """Test adding multiple nodes with same name (e.g., overloaded functions)."""
        graph = CodeGraph("test.py")
        node1 = create_function_node("func", 10, 5, "test.py")
        node2 = create_function_node("func", 20, 5, "test.py")
        
        graph.add_node(node1)
        graph.add_node(node2)
        
        assert len(graph.nodes) == 2
        assert len(graph.by_name["func"]) == 2
    
    def test_get_node(self):
        """Test retrieving node by ID."""
        graph = CodeGraph("test.py")
        node = create_function_node("test_func", 10, 5, "test.py")
        graph.add_node(node)
        
        retrieved = graph.get_node(node.id)
        
        assert retrieved is not None
        assert retrieved.id == node.id
        assert retrieved.name == "test_func"
    
    def test_get_node_nonexistent(self):
        """Test retrieving nonexistent node."""
        graph = CodeGraph("test.py")
        
        retrieved = graph.get_node("nonexistent_id")
        
        assert retrieved is None
    
    def test_get_nodes_by_name(self):
        """Test retrieving nodes by name."""
        graph = CodeGraph("test.py")
        node1 = create_function_node("func", 10, 5, "test.py")
        node2 = create_function_node("func", 20, 5, "test.py")
        graph.add_node(node1)
        graph.add_node(node2)
        
        nodes = graph.get_nodes_by_name("func")
        
        assert len(nodes) == 2
        assert node1 in nodes
        assert node2 in nodes
    
    def test_get_functions(self):
        """Test getting all function nodes."""
        graph = CodeGraph("test.py")
        func_node = create_function_node("func", 10, 5, "test.py")
        class_node = create_class_node("Class", 5, 0, "test.py")
        var_node = create_variable_node("x", 15, 4, "test.py")
        
        graph.add_node(func_node)
        graph.add_node(class_node)
        graph.add_node(var_node)
        
        functions = graph.get_functions()
        
        assert len(functions) == 1
        assert functions[0].name == "func"
    
    def test_get_classes(self):
        """Test getting all class nodes."""
        graph = CodeGraph("test.py")
        func_node = create_function_node("func", 10, 5, "test.py")
        class_node = create_class_node("Class", 5, 0, "test.py")
        var_node = create_variable_node("x", 15, 4, "test.py")
        
        graph.add_node(func_node)
        graph.add_node(class_node)
        graph.add_node(var_node)
        
        classes = graph.get_classes()
        
        assert len(classes) == 1
        assert classes[0].name == "Class"
    
    def test_get_variables(self):
        """Test getting all variable nodes."""
        graph = CodeGraph("test.py")
        func_node = create_function_node("func", 10, 5, "test.py")
        class_node = create_class_node("Class", 5, 0, "test.py")
        var_node = create_variable_node("x", 15, 4, "test.py")
        
        graph.add_node(func_node)
        graph.add_node(class_node)
        graph.add_node(var_node)
        
        variables = graph.get_variables()
        
        assert len(variables) == 1
        assert variables[0].name == "x"
    
    def test_graph_to_dict(self):
        """Test graph serialization to dictionary."""
        graph = CodeGraph("test.py")
        graph.language = "python"
        node = create_function_node("func", 10, 5, "test.py")
        graph.add_node(node)
        
        graph_dict = graph.to_dict()
        
        assert graph_dict['file_path'] == "test.py"
        assert graph_dict['language'] == "python"
        assert len(graph_dict['nodes']) == 1
        assert 'func' in graph_dict['by_name']


class TestGraphBuilding:
    """Test building graphs from parsed data."""
    
    def test_build_simple_graph(self):
        """Test building graph from simple parsed data."""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': 'def func():\n    pass\n',
            'functions': [
                {'name': 'func', 'line': 1, 'column': 0, 'parameters': [], 'body_start': 1, 'body_end': 2}
            ],
            'classes': [],
            'variables': []
        }
        
        graph = build_code_graph(parsed_data)
        
        assert graph.file_path == 'test.py'
        assert graph.language == 'python'
        assert len(graph.get_functions()) == 1
        assert graph.get_functions()[0].name == 'func'
    
    def test_build_graph_with_classes(self):
        """Test building graph with classes (mapped to MODULE per ARCHITECTURE)."""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': 'class MyClass:\n    pass\n',
            'functions': [],
            'classes': [
                {'name': 'MyClass', 'line': 1, 'column': 0, 'base_class': None}
            ],
            'variables': []
        }
        
        graph = build_code_graph(parsed_data)
        
        # Should have 1 class + 1 module node for the file itself (both are MODULE type per ARCHITECTURE)
        assert len(graph.get_classes()) == 2
        # Filter out the file module node to get actual class count
        actual_classes = [c for c in graph.get_classes() if c.name != 'test.py']
        assert len(actual_classes) == 1
        assert actual_classes[0].name == 'MyClass'
    
    def test_build_graph_with_variables(self):
        """Test building graph with variables."""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': 'x = 42\n',
            'functions': [],
            'classes': [],
            'variables': [
                {'name': 'x', 'line': 1, 'column': 0, 'value': '42'}
            ]
        }
        
        graph = build_code_graph(parsed_data)
        
        assert len(graph.get_variables()) == 1
        assert graph.get_variables()[0].name == 'x'
    
    def test_build_graph_with_function_calls(self):
        """Test building graph with function call relationships."""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': '''def func_a():
    func_b()

def func_b():
    pass
''',
            'functions': [
                {'name': 'func_a', 'line': 1, 'column': 0, 'parameters': [], 'body_start': 1, 'body_end': 2},
                {'name': 'func_b', 'line': 4, 'column': 0, 'parameters': [], 'body_start': 4, 'body_end': 5}
            ],
            'classes': [],
            'variables': []
        }
        
        graph = build_code_graph(parsed_data)
        
        func_a = graph.get_functions()[0]
        func_b = graph.get_functions()[1]
        
        # func_a should call func_b
        assert func_b.id in func_a.callees
        # func_b should be called by func_a
        assert func_a.id in func_b.callers
    
    def test_build_graph_with_class_inheritance(self):
        """Test building graph with class inheritance (coupled_with edge per ARCHITECTURE)."""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': '''class Parent:
    pass

class Child(Parent):
    pass
''',
            'functions': [],
            'classes': [
                {'name': 'Parent', 'line': 1, 'column': 0, 'base_class': None},
                {'name': 'Child', 'line': 4, 'column': 0, 'base_class': 'Parent'}
            ],
            'variables': []
        }
        
        graph = build_code_graph(parsed_data)
        
        # Filter out file module node (mapped to MODULE per ARCHITECTURE)
        actual_classes = [c for c in graph.get_classes() if c.name != 'test.py']
        parent = actual_classes[0]
        child = actual_classes[1]
        
        # Child should have coupled_with edge to Parent per ARCHITECTURE
        from core.graph.nodes import EdgeType
        assert parent.id in child.edges[EdgeType.COUPLED_WITH]
        # Parent should be inherited by Child (stored in meta)
        assert child.id in parent.meta.get('inherited_by', [])


class TestGraphRelationships:
    """Test graph relationship tracking."""
    
    def test_function_call_tracking(self):
        """Test that function calls are tracked correctly."""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': '''def main():
    helper()
    another_helper()

def helper():
    pass

def another_helper():
    pass
''',
            'functions': [
                {'name': 'main', 'line': 1, 'column': 0, 'parameters': [], 'body_start': 1, 'body_end': 3},
                {'name': 'helper', 'line': 5, 'column': 0, 'parameters': [], 'body_start': 5, 'body_end': 6},
                {'name': 'another_helper', 'line': 8, 'column': 0, 'parameters': [], 'body_start': 8, 'body_end': 9}
            ],
            'classes': [],
            'variables': []
        }
        
        graph = build_code_graph(parsed_data)
        
        main_func = [f for f in graph.get_functions() if f.name == 'main'][0]
        helper_func = [f for f in graph.get_functions() if f.name == 'helper'][0]
        another_func = [f for f in graph.get_functions() if f.name == 'another_helper'][0]
        
        # main should call both helpers
        assert helper_func.id in main_func.callees
        assert another_func.id in main_func.callees
        assert len(main_func.callees) == 2
    
    def test_no_self_calls(self):
        """Test that functions don't track calls to themselves."""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': '''def recursive():
    recursive()
''',
            'functions': [
                {'name': 'recursive', 'line': 1, 'column': 0, 'parameters': [], 'body_start': 1, 'body_end': 2}
            ],
            'classes': [],
            'variables': []
        }
        
        graph = build_code_graph(parsed_data)
        
        func = graph.get_functions()[0]
        
        # Should not track self-calls
        assert func.id not in func.callees


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
