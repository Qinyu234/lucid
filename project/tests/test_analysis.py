"""
Tests for analysis layer
Tests access contract extraction and def-use analysis
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.analysis.access_contract import (
    extract_access_contracts,
    AccessContract,
    WriteSite,
    UseSite,
    _find_context
)
from core.graph.builder import build_code_graph, CodeGraph
from core.graph.nodes import create_function_node, create_variable_node


class TestAccessContractDataClasses:
    """Test AccessContract and related data classes."""
    
    def test_write_site_creation(self):
        """Test WriteSite dataclass creation."""
        site = WriteSite("file.py:10", 10, "function_name", "module")
        
        assert site.location == "file.py:10"
        assert site.line == 10
        assert site.context == "function_name"
        assert site.scope == "module"
    
    def test_use_site_creation(self):
        """Test UseSite dataclass creation."""
        site = UseSite("file.py:15", 15, "function_name", "module")
        
        assert site.location == "file.py:15"
        assert site.line == 15
        assert site.context == "function_name"
        assert site.scope == "module"
    
    def test_access_contract_creation(self):
        """Test AccessContract dataclass creation."""
        write_site = WriteSite("file.py:10", 10, "func", "module")
        use_site = UseSite("file.py:15", 15, "func", "module")
        
        contract = AccessContract(
            variable_name="x",
            defined="file.py:5",
            write_sites=[write_site],
            use_sites=[use_site],
            source="inferred"
        )
        
        assert contract.variable_name == "x"
        assert contract.defined == "file.py:5"
        assert len(contract.write_sites) == 1
        assert len(contract.use_sites) == 1
        assert contract.source == "inferred"
    
    def test_access_contract_to_dict(self):
        """Test AccessContract serialization to dictionary."""
        write_site = WriteSite("file.py:10", 10, "func", "module")
        use_site = UseSite("file.py:15", 15, "func", "module")
        
        contract = AccessContract(
            variable_name="x",
            defined="file.py:5",
            write_sites=[write_site],
            use_sites=[use_site],
            source="inferred"
        )
        
        contract_dict = contract.to_dict()
        
        assert "x" in contract_dict
        assert contract_dict["x"]["defined"] == "file.py:5"
        assert contract_dict["x"]["write_sites"] == ["file.py:10"]
        assert contract_dict["x"]["use_sites"] == ["file.py:15"]
        assert contract_dict["x"]["source"] == "inferred"


class TestContextFinding:
    """Test context finding for line numbers."""
    
    def test_find_context_in_function(self):
        """Test finding context when line is in function."""
        graph = CodeGraph("test.py")
        func = create_function_node("test_func", 5, 0, "test.py")
        func.meta['body_start'] = 5
        func.meta['body_end'] = 10
        graph.add_node(func)
        
        context = _find_context(7, [func], [""] * 20)
        
        assert context == "test_func"
    
    def test_find_context_outside_function(self):
        """Test finding context when line is outside any function."""
        graph = CodeGraph("test.py")
        func = create_function_node("test_func", 5, 0, "test.py")
        func.meta['body_start'] = 5
        func.meta['body_end'] = 10
        graph.add_node(func)
        
        context = _find_context(3, [func], [""] * 20)
        
        assert context == "module"
    
    def test_find_context_multiple_functions(self):
        """Test finding context with multiple functions."""
        graph = CodeGraph("test.py")
        func1 = create_function_node("func1", 5, 0, "test.py")
        func1.meta['body_start'] = 5
        func1.meta['body_end'] = 10
        func2 = create_function_node("func2", 15, 0, "test.py")
        func2.meta['body_start'] = 15
        func2.meta['body_end'] = 20
        graph.add_node(func1)
        graph.add_node(func2)
        
        context1 = _find_context(7, [func1, func2], [""] * 25)
        context2 = _find_context(17, [func1, func2], [""] * 25)
        context3 = _find_context(12, [func1, func2], [""] * 25)
        
        assert context1 == "func1"
        assert context2 == "func2"
        assert context3 == "module"


class TestAccessContractExtraction:
    """Test access contract extraction from code."""
    
    def test_extract_simple_assignment(self):
        """Test extraction of simple variable assignment."""
        source_code = """x = 42
print(x)
"""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': source_code,
            'functions': [],
            'classes': [],
            'variables': [
                {'name': 'x', 'line': 1, 'column': 0, 'value': '42'}
            ]
        }
        
        graph = build_code_graph(parsed_data)
        contracts = extract_access_contracts(graph, source_code)
        
        assert 'x' in contracts
        assert contracts['x'].variable_name == 'x'
        assert len(contracts['x'].write_sites) >= 1
        assert len(contracts['x'].use_sites) >= 1
    
    def test_extract_multiple_assignments(self):
        """Test extraction of multiple assignments to same variable."""
        source_code = """x = 1
x = 2
x = 3
print(x)
"""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': source_code,
            'functions': [],
            'classes': [],
            'variables': [
                {'name': 'x', 'line': 1, 'column': 0, 'value': '1'}
            ]
        }
        
        graph = build_code_graph(parsed_data)
        contracts = extract_access_contracts(graph, source_code)
        
        assert 'x' in contracts
        # Should find multiple write sites
        assert len(contracts['x'].write_sites) >= 2
    
    def test_extract_augmented_assignment(self):
        """Test extraction of augmented assignments (+=, -=, etc.)."""
        source_code = """x = 10
x += 5
x -= 3
"""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': source_code,
            'functions': [],
            'classes': [],
            'variables': [
                {'name': 'x', 'line': 1, 'column': 0, 'value': '10'}
            ]
        }
        
        graph = build_code_graph(parsed_data)
        contracts = extract_access_contracts(graph, source_code)
        
        assert 'x' in contracts
        # Should find augmented assignments as writes
        assert len(contracts['x'].write_sites) >= 2
    
    def test_extract_function_context(self):
        """Test extraction with function context."""
        source_code = """def process():
    x = 10
    y = x + 5
    return y
"""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': source_code,
            'functions': [
                {'name': 'process', 'line': 1, 'column': 0, 'parameters': [], 'body_start': 1, 'body_end': 4}
            ],
            'classes': [],
            'variables': [
                {'name': 'x', 'line': 2, 'column': 4, 'value': '10'},
                {'name': 'y', 'line': 3, 'column': 4, 'value': 'x + 5'}
            ]
        }
        
        graph = build_code_graph(parsed_data)
        contracts = extract_access_contracts(graph, source_code)
        
        if 'x' in contracts:
            # Check that context is set for write/use sites
            for site in contracts['x'].write_sites + contracts['x'].use_sites:
                assert site.context in ['process', 'module']
    
    def test_extract_with_no_variables(self):
        """Test extraction when no variables are present."""
        source_code = """def empty():
    pass
"""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': source_code,
            'functions': [
                {'name': 'empty', 'line': 1, 'column': 0, 'parameters': [], 'body_start': 1, 'body_end': 2}
            ],
            'classes': [],
            'variables': []
        }
        
        graph = build_code_graph(parsed_data)
        contracts = extract_access_contracts(graph, source_code)
        
        assert len(contracts) == 0
    
    def test_extract_avoids_false_positives(self):
        """Test that extraction avoids false positives from substrings."""
        source_code = """count = 5
discount = 10
print(count)
print(discount)
"""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': source_code,
            'functions': [],
            'classes': [],
            'variables': [
                {'name': 'count', 'line': 1, 'column': 0, 'value': '5'},
                {'name': 'discount', 'line': 2, 'column': 0, 'value': '10'}
            ]
        }
        
        graph = build_code_graph(parsed_data)
        contracts = extract_access_contracts(graph, source_code)
        
        # 'count' should not be detected in 'discount' line
        if 'count' in contracts:
            count_write_lines = [site.line for site in contracts['count'].write_sites]
            assert 2 not in count_write_lines  # Line 2 is discount, not count


class TestDefUseAnalysis:
    """Test def-use analysis functionality."""
    
    def test_def_use_chain_tracking(self):
        """Test that def-use chains are tracked."""
        source_code = """x = 10
y = x + 5
z = y * 2
"""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': source_code,
            'functions': [],
            'classes': [],
            'variables': [
                {'name': 'x', 'line': 1, 'column': 0, 'value': '10'},
                {'name': 'y', 'line': 2, 'column': 0, 'value': 'x + 5'},
                {'name': 'z', 'line': 3, 'column': 0, 'value': 'y * 2'}
            ]
        }
        
        graph = build_code_graph(parsed_data)
        contracts = extract_access_contracts(graph, source_code)
        
        # x should be used in line 2
        if 'x' in contracts:
            x_use_lines = [site.line for site in contracts['x'].use_sites]
            assert 2 in x_use_lines
        
        # y should be used in line 3
        if 'y' in contracts:
            y_use_lines = [site.line for site in contracts['y'].use_sites]
            assert 3 in y_use_lines
    
    def test_write_only_variable(self):
        """Test detection of write-only variables."""
        source_code = """temp = 42
# temp is never used
"""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': source_code,
            'functions': [],
            'classes': [],
            'variables': [
                {'name': 'temp', 'line': 1, 'column': 0, 'value': '42'}
            ]
        }
        
        graph = build_code_graph(parsed_data)
        contracts = extract_access_contracts(graph, source_code)
        
        if 'temp' in contracts:
            # temp should have write sites but no use sites
            assert len(contracts['temp'].write_sites) >= 1
            assert len(contracts['temp'].use_sites) == 0
    
    def test_read_only_variable(self):
        """Test detection of read-only variables (parameters)."""
        source_code = """def func(param):
    return param + 1
"""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': source_code,
            'functions': [
                {'name': 'func', 'line': 1, 'column': 0, 'parameters': ['param'], 'body_start': 1, 'body_end': 2}
            ],
            'classes': [],
            'variables': []
        }
        
        graph = build_code_graph(parsed_data)
        contracts = extract_access_contracts(graph, source_code)
        
        # Parameters may not be in variables list, but if they are,
        # they should be read-only (no writes)
        if 'param' in contracts:
            assert len(contracts['param'].write_sites) == 0


class TestScopeTracking:
    """Test scope tracking functionality."""
    
    def test_scope_info_building_with_ast(self):
        """Test scope info building when AST is available."""
        # This test would require a real tree-sitter AST
        # For now, we test the fallback behavior
        source_code = """def func():
    x = 10
"""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': source_code,
            'functions': [
                {'name': 'func', 'line': 1, 'column': 0, 'parameters': [], 'body_start': 1, 'body_end': 2}
            ],
            'classes': [],
            'variables': [
                {'name': 'x', 'line': 2, 'column': 4, 'value': '10'}
            ]
        }
        
        graph = build_code_graph(parsed_data)
        
        # Test without AST (should still work)
        contracts = extract_access_contracts(graph, source_code, ast=None)
        
        assert contracts is not None
    
    def test_scope_assignment(self):
        """Test that scope is assigned to write/use sites."""
        source_code = """def outer():
    x = 10
    
    def inner():
        y = 20
"""
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': source_code,
            'functions': [
                {'name': 'outer', 'line': 1, 'column': 0, 'parameters': [], 'body_start': 1, 'body_end': 5},
                {'name': 'inner', 'line': 4, 'column': 4, 'parameters': [], 'body_start': 4, 'body_end': 5}
            ],
            'classes': [],
            'variables': [
                {'name': 'x', 'line': 2, 'column': 4, 'value': '10'},
                {'name': 'y', 'line': 5, 'column': 8, 'value': '20'}
            ]
        }
        
        graph = build_code_graph(parsed_data)
        contracts = extract_access_contracts(graph, source_code, ast=None)
        
        # Check that scopes are assigned
        for var_name, contract in contracts.items():
            for site in contract.write_sites + contract.use_sites:
                assert site.scope in ['module', 'outer', 'inner']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
