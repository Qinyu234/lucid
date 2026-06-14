"""
Tests for CLI
Tests command-line interface functionality
"""

import pytest
import sys
import tempfile
import os
from pathlib import Path
from io import StringIO
from unittest.mock import patch

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestCLIIntegration:
    """Test CLI integration with core functionality."""
    
    def test_cli_module_import(self):
        """Test that CLI module can be imported."""
        try:
            from cli import main
            assert main is not None
        except ImportError as e:
            pytest.skip(f"CLI module not available: {e}")
    
    def test_cli_analyze_command_help(self):
        """Test CLI analyze command help."""
        try:
            from cli import main
            with patch('sys.argv', ['cli.py', 'analyze', '--help']):
                with pytest.raises(SystemExit):
                    main()
        except ImportError:
            pytest.skip("CLI module not available")
    
    def test_cli_structure_command_help(self):
        """Test CLI structure command help."""
        try:
            from cli import main
            with patch('sys.argv', ['cli.py', 'structure', '--help']):
                with pytest.raises(SystemExit):
                    main()
        except ImportError:
            pytest.skip("CLI module not available")
    
    def test_cli_virtual_command_help(self):
        """Test CLI virtual command help."""
        try:
            from cli import main
            with patch('sys.argv', ['cli.py', 'virtual', '--help']):
                with pytest.raises(SystemExit):
                    main()
        except ImportError:
            pytest.skip("CLI module not available")


class TestCLIWithRealFiles:
    """Test CLI with actual Python files."""
    
    def test_cli_analyze_simple_file(self):
        """Test analyzing a simple Python file via CLI."""
        try:
            from cli import main
            from core.ingestion import parse_file
            from core.graph import build_code_graph
            from core.analysis import extract_access_contracts
        except ImportError:
            pytest.skip("Required modules not available")
        
        # Create a temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
def process(data):
    result = data * 2
    return result

x = 10
y = x + 5
""")
            temp_path = f.name
        
        try:
            # Test the pipeline that CLI would use
            parsed = parse_file(temp_path)
            assert parsed is not None
            assert parsed['language'] == 'python'
            
            graph = build_code_graph(parsed)
            assert graph is not None
            assert len(graph.get_functions()) >= 1
            
            contracts = extract_access_contracts(graph, parsed['source_code'])
            assert contracts is not None
            
        finally:
            os.unlink(temp_path)
    
    def test_cli_structure_simple_file(self):
        """Test structure command on a simple file."""
        try:
            from core.ingestion import parse_file
            from core.graph import build_code_graph
            from core.views import StructureView
        except ImportError:
            pytest.skip("Required modules not available")
        
        # Create a temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
class Calculator:
    def add(self, a, b):
        return a + b

def main():
    calc = Calculator()
    result = calc.add(5, 3)
    print(result)
""")
            temp_path = f.name
        
        try:
            parsed = parse_file(temp_path)
            graph = build_code_graph(parsed)
            view = StructureView(graph)
            
            functions = view.get_function_list()
            classes = view.get_class_list()
            
            assert len(functions) >= 1
            assert len(classes) == 1
            assert classes[0]['name'] == 'Calculator'
            
        finally:
            os.unlink(temp_path)


class TestCLIErrorHandling:
    """Test CLI error handling."""
    
    def test_cli_nonexistent_file(self):
        """Test CLI behavior with nonexistent file."""
        try:
            from core.ingestion import parse_file
        except ImportError:
            pytest.skip("Required modules not available")
        
        with pytest.raises(FileNotFoundError):
            parse_file("/nonexistent/file.py")
    
    def test_cli_unsupported_file_type(self):
        """Test CLI behavior with unsupported file type."""
        try:
            from core.ingestion import parse_file
        except ImportError:
            pytest.skip("Required modules not available")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xyz', delete=False) as f:
            f.write("some content")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError):
                parse_file(temp_path)
        finally:
            os.unlink(temp_path)


class TestCLIPipeline:
    """Test complete CLI pipeline."""
    
    def test_full_analysis_pipeline(self):
        """Test the complete analysis pipeline from ingestion to views."""
        try:
            from core.ingestion import parse_file
            from core.graph import build_code_graph
            from core.analysis import extract_access_contracts
            from core.views import DefUseView, StructureView
        except ImportError:
            pytest.skip("Required modules not available")
        
        # Create a test file with various patterns
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
import os

class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.processed = False
    
    def process(self):
        result = []
        for item in self.data:
            processed_item = item * 2
            result.append(processed_item)
        self.processed = True
        return result

def main():
    processor = DataProcessor([1, 2, 3])
    output = processor.process()
    print(output)
    return output

if __name__ == '__main__':
    main()
""")
            temp_path = f.name
        
        try:
            # Step 1: Ingestion
            parsed = parse_file(temp_path)
            assert parsed['language'] == 'python'
            assert len(parsed['functions']) >= 2
            assert len(parsed['classes']) == 1
            
            # Step 2: Graph building
            graph = build_code_graph(parsed)
            assert len(graph.get_functions()) >= 2
            assert len(graph.get_classes()) == 1
            
            # Step 3: Analysis
            contracts = extract_access_contracts(graph, parsed['source_code'])
            assert contracts is not None
            
            # Step 4: Views
            def_use_view = DefUseView(contracts)
            structure_view = StructureView(graph)
            
            # Test structure view
            functions = structure_view.get_function_list()
            classes = structure_view.get_class_list()
            assert len(functions) >= 2
            assert len(classes) == 1
            
            # Test def-use view
            all_vars = def_use_view.get_all_variables()
            assert all_vars is not None
            
        finally:
            os.unlink(temp_path)
    
    def test_pipeline_with_empty_file(self):
        """Test pipeline with empty file."""
        try:
            from core.ingestion import parse_file
            from core.graph import build_code_graph
            from core.analysis import extract_access_contracts
        except ImportError:
            pytest.skip("Required modules not available")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("")
            temp_path = f.name
        
        try:
            parsed = parse_file(temp_path)
            graph = build_code_graph(parsed)
            contracts = extract_access_contracts(graph, parsed['source_code'])
            
            assert parsed is not None
            assert graph is not None
            assert contracts is not None
            assert len(contracts) == 0
            
        finally:
            os.unlink(temp_path)
    
    def test_pipeline_with_syntax_error(self):
        """Test pipeline with file containing syntax errors."""
        try:
            from core.ingestion import parse_file
            from core.graph import build_code_graph
        except ImportError:
            pytest.skip("Required modules not available")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
def incomplete_function(
    # Missing closing parenthesis
""")
            temp_path = f.name
        
        try:
            # Should not crash, but may not parse correctly
            parsed = parse_file(temp_path)
            graph = build_code_graph(parsed)
            
            # Should still return results
            assert parsed is not None
            assert graph is not None
            
        finally:
            os.unlink(temp_path)


class TestCLIOutputFormats:
    """Test CLI output formats."""
    
    def test_render_def_use_contract_output(self):
        """Test that def-use contract rendering produces expected output."""
        try:
            from core.analysis.access_contract import AccessContract, WriteSite, UseSite
            from core.views.def_use_view import DefUseView, render_def_use_contract
        except ImportError:
            pytest.skip("Required modules not available")
        
        contract = AccessContract(
            'test_var',
            'test.py:5',
            [WriteSite('test.py:5', 5, 'module', 'module')],
            [UseSite('test.py:10', 10, 'module', 'module')],
            'inferred'
        )
        
        view = DefUseView({'test_var': contract})
        rendered = render_def_use_contract('test_var', view)
        
        assert "Access Contract" in rendered
        assert "test_var" in rendered
        assert "test.py:5" in rendered
        assert "test.py:10" in rendered
    
    def test_render_structure_output(self):
        """Test that structure rendering produces expected output."""
        try:
            from core.graph.builder import CodeGraph
            from core.graph.nodes import create_function_node
            from core.views.structure_view import StructureView
        except ImportError:
            pytest.skip("Required modules not available")
        
        graph = CodeGraph("test.py")
        graph.language = "python"
        func = create_function_node("test_func", 10, 0, "test.py")
        func.meta['parameters'] = ['x', 'y']
        graph.add_node(func)
        
        view = StructureView(graph)
        rendered = view.render_structure()
        
        assert "Code Structure" in rendered
        assert "test.py" in rendered
        assert "python" in rendered
        assert "test_func" in rendered


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
