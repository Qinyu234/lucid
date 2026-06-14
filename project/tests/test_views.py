"""
Tests for views layer
Tests Def-Use view and Structure view functionality
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.views.def_use_view import DefUseView, render_def_use_contract, render_summary
from core.views.structure_view import StructureView
from core.analysis.access_contract import AccessContract, WriteSite, UseSite
from core.graph.builder import build_code_graph, CodeGraph
from core.graph.nodes import create_function_node, create_class_node, create_variable_node


class TestDefUseView:
    """Test Def-Use Contract view functionality."""
    
    def test_view_initialization(self):
        """Test DefUseView initialization."""
        contracts = {
            'x': AccessContract(
                variable_name='x',
                defined='test.py:1',
                write_sites=[WriteSite('test.py:1', 1, 'module', 'module')],
                use_sites=[UseSite('test.py:2', 2, 'module', 'module')],
                source='inferred'
            )
        }
        
        view = DefUseView(contracts)
        
        assert len(view.get_all_variables()) == 1
        assert 'x' in view.get_all_variables()
    
    def test_get_variable_info_found(self):
        """Test getting info for existing variable."""
        contracts = {
            'x': AccessContract(
                variable_name='x',
                defined='test.py:1',
                write_sites=[WriteSite('test.py:1', 1, 'module', 'module')],
                use_sites=[UseSite('test.py:2', 2, 'module', 'module')],
                source='inferred'
            )
        }
        
        view = DefUseView(contracts)
        info = view.get_variable_info('x')
        
        assert info['variable'] == 'x'
        assert info['found'] is True
        assert info['defined'] == 'test.py:1'
        assert info['write_count'] == 1
        assert info['use_count'] == 1
    
    def test_get_variable_info_not_found(self):
        """Test getting info for nonexistent variable."""
        contracts = {}
        view = DefUseView(contracts)
        info = view.get_variable_info('nonexistent')
        
        assert info['variable'] == 'nonexistent'
        assert info['found'] is False
    
    def test_get_all_variables(self):
        """Test getting all variable names."""
        contracts = {
            'x': AccessContract('x', 'test.py:1', [], [], 'inferred'),
            'y': AccessContract('y', 'test.py:2', [], [], 'inferred'),
            'z': AccessContract('z', 'test.py:3', [], [], 'inferred')
        }
        
        view = DefUseView(contracts)
        variables = view.get_all_variables()
        
        assert len(variables) == 3
        assert 'x' in variables
        assert 'y' in variables
        assert 'z' in variables
    
    def test_get_high_impact_variables(self):
        """Test getting high impact variables (used many times)."""
        contracts = {
            'high_impact': AccessContract(
                'high_impact',
                'test.py:1',
                [WriteSite('test.py:1', 1, 'module', 'module')],
                [UseSite('test.py:2', 2, 'module', 'module'),
                 UseSite('test.py:3', 3, 'module', 'module'),
                 UseSite('test.py:4', 4, 'module', 'module'),
                 UseSite('test.py:5', 5, 'module', 'module'),
                 UseSite('test.py:6', 6, 'module', 'module')],
                'inferred'
            ),
            'low_impact': AccessContract(
                'low_impact',
                'test.py:10',
                [WriteSite('test.py:10', 10, 'module', 'module')],
                [UseSite('test.py:11', 11, 'module', 'module')],
                'inferred'
            )
        }
        
        view = DefUseView(contracts)
        high_impact = view.get_high_impact_variables(threshold=3)
        
        assert len(high_impact) == 1
        assert 'high_impact' in high_impact
        assert 'low_impact' not in high_impact
    
    def test_get_high_impact_variables_sorted(self):
        """Test that high impact variables are sorted by use count."""
        contracts = {
            'var3': AccessContract('var3', 'test.py:1', [], 
                                   [UseSite('test.py:2', 2, 'module', 'module')] * 3, 'inferred'),
            'var5': AccessContract('var5', 'test.py:1', [], 
                                   [UseSite('test.py:2', 2, 'module', 'module')] * 5, 'inferred'),
            'var4': AccessContract('var4', 'test.py:1', [], 
                                   [UseSite('test.py:2', 2, 'module', 'module')] * 4, 'inferred')
        }
        
        view = DefUseView(contracts)
        high_impact = view.get_high_impact_variables(threshold=2)
        
        # Should be sorted by use count (descending)
        assert high_impact[0] == 'var5'
        assert high_impact[1] == 'var4'
        assert high_impact[2] == 'var3'
    
    def test_get_write_only_variables(self):
        """Test getting write-only variables."""
        contracts = {
            'write_only': AccessContract(
                'write_only',
                'test.py:1',
                [WriteSite('test.py:1', 1, 'module', 'module')],
                [],
                'inferred'
            ),
            'read_write': AccessContract(
                'read_write',
                'test.py:2',
                [WriteSite('test.py:2', 2, 'module', 'module')],
                [UseSite('test.py:3', 3, 'module', 'module')],
                'inferred'
            )
        }
        
        view = DefUseView(contracts)
        write_only = view.get_write_only_variables()
        
        assert len(write_only) == 1
        assert 'write_only' in write_only
        assert 'read_write' not in write_only


class TestRenderDefUseContract:
    """Test rendering of def-use contracts."""
    
    def test_render_found_variable(self):
        """Test rendering access contract for found variable."""
        contracts = {
            'x': AccessContract(
                'x',
                'test.py:1',
                [WriteSite('test.py:1', 1, 'module', 'module')],
                [UseSite('test.py:2', 2, 'module', 'module')],
                'inferred'
            )
        }
        view = DefUseView(contracts)
        
        rendered = render_def_use_contract('x', view)
        
        assert "Access Contract for 'x'" in rendered
        assert "test.py:1" in rendered
        assert "Write Sites" in rendered
        assert "Use Sites" in rendered
        assert "inferred" in rendered
    
    def test_render_not_found_variable(self):
        """Test rendering access contract for nonexistent variable."""
        contracts = {}
        view = DefUseView(contracts)
        
        rendered = render_def_use_contract('nonexistent', view)
        
        assert "not found" in rendered.lower()
    
    def test_render_multiple_write_sites(self):
        """Test rendering with multiple write sites."""
        contracts = {
            'x': AccessContract(
                'x',
                'test.py:1',
                [WriteSite('test.py:1', 1, 'module', 'module'),
                 WriteSite('test.py:5', 5, 'module', 'module'),
                 WriteSite('test.py:10', 10, 'module', 'module')],
                [UseSite('test.py:2', 2, 'module', 'module')],
                'inferred'
            )
        }
        view = DefUseView(contracts)
        
        rendered = render_def_use_contract('x', view)
        
        assert "test.py:1" in rendered
        assert "test.py:5" in rendered
        assert "test.py:10" in rendered


class TestRenderSummary:
    """Test rendering of access contract summary."""
    
    def test_render_summary_basic(self):
        """Test basic summary rendering."""
        contracts = {
            'x': AccessContract('x', 'test.py:1', [], [], 'inferred'),
            'y': AccessContract('y', 'test.py:2', [], [], 'inferred')
        }
        view = DefUseView(contracts)
        
        summary = render_summary(view)
        
        assert "Access Contract Summary" in summary
        assert "2 variables" in summary or "Total variables analyzed: 2" in summary
    
    def test_render_summary_with_high_impact(self):
        """Test summary with high impact variables."""
        contracts = {
            'high': AccessContract(
                'high',
                'test.py:1',
                [],
                [UseSite('test.py:2', 2, 'module', 'module')] * 5,
                'inferred'
            ),
            'low': AccessContract(
                'low',
                'test.py:3',
                [],
                [UseSite('test.py:4', 4, 'module', 'module')],
                'inferred'
            )
        }
        view = DefUseView(contracts)
        
        summary = render_summary(view)
        
        assert "High Impact Variables" in summary
        assert "high" in summary.lower()
    
    def test_render_summary_with_write_only(self):
        """Test summary with write-only variables."""
        contracts = {
            'write_only': AccessContract(
                'write_only',
                'test.py:1',
                [WriteSite('test.py:1', 1, 'module', 'module')],
                [],
                'inferred'
            )
        }
        view = DefUseView(contracts)
        
        summary = render_summary(view)
        
        assert "Write-Only Variables" in summary
        assert "write_only" in summary


class TestStructureView:
    """Test Structure view functionality."""
    
    def test_structure_view_initialization(self):
        """Test StructureView initialization."""
        graph = CodeGraph("test.py")
        view = StructureView(graph)
        
        assert view.graph == graph
    
    def test_get_function_list(self):
        """Test getting function list."""
        graph = CodeGraph("test.py")
        func = create_function_node("func1", 5, 0, "test.py")
        func.meta['parameters'] = ['a', 'b']
        graph.add_node(func)
        
        view = StructureView(graph)
        functions = view.get_function_list()
        
        assert len(functions) == 1
        assert functions[0]['name'] == 'func1'
        assert functions[0]['line'] == 5
        assert functions[0]['parameters'] == ['a', 'b']
    
    def test_get_class_list(self):
        """Test getting class list."""
        graph = CodeGraph("test.py")
        cls = create_class_node("MyClass", 10, 0, "test.py", "BaseClass")
        graph.add_node(cls)
        
        view = StructureView(graph)
        classes = view.get_class_list()
        
        assert len(classes) == 1
        assert classes[0]['name'] == 'MyClass'
        assert classes[0]['line'] == 10
        assert classes[0]['base_class'] == 'BaseClass'
    
    def test_get_variable_list(self):
        """Test getting variable list."""
        graph = CodeGraph("test.py")
        var = create_variable_node("x", 15, 4, "test.py", "42")
        graph.add_node(var)
        
        view = StructureView(graph)
        variables = view.get_variable_list()
        
        assert len(variables) == 1
        assert variables[0]['name'] == 'x'
        assert variables[0]['line'] == 15
        assert variables[0]['initial_value'] == '42'
    
    def test_render_structure_empty(self):
        """Test rendering structure with no nodes."""
        graph = CodeGraph("test.py")
        graph.language = "python"
        view = StructureView(graph)
        
        rendered = view.render_structure()
        
        assert "Code Structure" in rendered
        assert "test.py" in rendered
        assert "python" in rendered
    
    def test_render_structure_with_functions(self):
        """Test rendering structure with functions."""
        graph = CodeGraph("test.py")
        graph.language = "python"
        func = create_function_node("test_func", 5, 0, "test.py")
        func.meta['parameters'] = ['x', 'y']
        graph.add_node(func)
        
        view = StructureView(graph)
        rendered = view.render_structure()
        
        assert "Functions" in rendered
        assert "test_func" in rendered
        assert "x, y" in rendered
    
    def test_render_structure_with_classes(self):
        """Test rendering structure with classes."""
        graph = CodeGraph("test.py")
        graph.language = "python"
        cls = create_class_node("MyClass", 5, 0, "test.py", "BaseClass")
        graph.add_node(cls)
        
        view = StructureView(graph)
        rendered = view.render_structure()
        
        assert "Classes" in rendered
        assert "MyClass" in rendered
        assert "BaseClass" in rendered
    
    def test_render_structure_with_variables(self):
        """Test rendering structure with variables."""
        graph = CodeGraph("test.py")
        graph.language = "python"
        var = create_variable_node("count", 10, 4, "test.py", "0")
        graph.add_node(var)
        
        view = StructureView(graph)
        rendered = view.render_structure()
        
        assert "Variables" in rendered
        assert "count" in rendered
        assert "= 0" in rendered
    
    def test_render_structure_complete(self):
        """Test rendering complete structure."""
        graph = CodeGraph("test.py")
        graph.language = "python"
        
        func = create_function_node("process", 5, 0, "test.py")
        func.meta['parameters'] = ['data']
        graph.add_node(func)
        
        cls = create_class_node("Processor", 10, 0, "test.py")
        graph.add_node(cls)
        
        var = create_variable_node("result", 15, 4, "test.py", "None")
        graph.add_node(var)
        
        view = StructureView(graph)
        rendered = view.render_structure()
        
        assert "Functions" in rendered
        assert "Classes" in rendered
        assert "Variables" in rendered
        assert "process" in rendered
        assert "Processor" in rendered
        assert "result" in rendered


class TestViewsIntegration:
    """Test integration of different views."""
    
    def test_def_use_and_structure_views_same_graph(self):
        """Test that both views work with the same graph."""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': '''def process(data):
    result = data * 2
    return result
''',
            'functions': [
                {'name': 'process', 'line': 1, 'column': 0, 'parameters': ['data'], 'body_start': 1, 'body_end': 3}
            ],
            'classes': [],
            'variables': [
                {'name': 'result', 'line': 2, 'column': 4, 'value': 'data * 2'}
            ]
        }
        
        graph = build_code_graph(parsed_data)
        
        # Structure view
        structure_view = StructureView(graph)
        functions = structure_view.get_function_list()
        assert len(functions) == 1
        
        # Def-Use view (would need access contracts)
        # This tests that the graph is compatible with both views
        assert graph.get_functions() is not None
        assert graph.get_variables() is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
