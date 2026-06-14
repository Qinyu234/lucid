"""
Tests for ingestion layer
Tests code parsing functionality for multiple languages
"""

import pytest
import tempfile
import os
from pathlib import Path

# Add project root to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.ingestion.parser import parse_file, parse_code_string, get_language


class TestLanguageDetection:
    """Test language detection from file extensions."""
    
    def test_python_detection(self):
        """Test Python file detection."""
        assert get_language("test.py") == "python"
        assert get_language("/path/to/file.py") == "python"
    
    def test_javascript_detection(self):
        """Test JavaScript file detection."""
        assert get_language("test.js") == "javascript"
        assert get_language("test.jsx") == "javascript"
    
    def test_typescript_detection(self):
        """Test TypeScript file detection."""
        assert get_language("test.ts") == "typescript"
        assert get_language("test.tsx") == "typescript"
    
    def test_go_detection(self):
        """Test Go file detection."""
        assert get_language("test.go") == "go"
    
    def test_rust_detection(self):
        """Test Rust file detection."""
        assert get_language("test.rs") == "rust"
    
    def test_unsupported_extension(self):
        """Test unsupported file extension."""
        assert get_language("test.xyz") is None
        assert get_language("test.txt") is None


class TestPythonParsing:
    """Test Python code parsing."""
    
    def test_simple_function_extraction(self):
        """Test extraction of simple function."""
        code = """
def hello_world():
    print("Hello, World!")
"""
        result = parse_code_string(code, "python", "test.py")
        
        assert len(result['functions']) == 1
        assert result['functions'][0]['name'] == 'hello_world'
        assert result['functions'][0]['line'] == 2
        assert 'parameters' in result['functions'][0]
    
    def test_function_with_parameters(self):
        """Test extraction of function with parameters."""
        code = """
def add(a, b, c):
    return a + b + c
"""
        result = parse_code_string(code, "python", "test.py")
        
        assert len(result['functions']) == 1
        assert result['functions'][0]['name'] == 'add'
        assert result['functions'][0]['parameters'] == ['a', 'b', 'c']
    
    def test_class_extraction(self):
        """Test extraction of class definition."""
        code = """
class MyClass:
    def __init__(self):
        self.value = 42
"""
        result = parse_code_string(code, "python", "test.py")
        
        assert len(result['classes']) == 1
        assert result['classes'][0]['name'] == 'MyClass'
        assert result['classes'][0]['line'] == 2
    
    def test_class_with_inheritance(self):
        """Test extraction of class with inheritance."""
        code = """
class ChildClass(ParentClass):
    pass
"""
        result = parse_code_string(code, "python", "test.py")
        
        assert len(result['classes']) == 1
        assert result['classes'][0]['name'] == 'ChildClass'
        # Note: Basic regex fallback may not capture base class
    
    def test_variable_assignment(self):
        """Test extraction of variable assignments."""
        code = """
x = 10
y = "hello"
z = x + 5
"""
        result = parse_code_string(code, "python", "test.py")
        
        # Should extract at least some variables
        assert len(result['variables']) >= 1
        variable_names = [v['name'] for v in result['variables']]
        assert 'x' in variable_names
    
    def test_import_extraction(self):
        """Test extraction of import statements."""
        code = """
import os
import sys
from pathlib import Path
"""
        result = parse_code_string(code, "python", "test.py")
        
        assert len(result['imports']) >= 2
        import_statements = [imp['statement'] for imp in result['imports']]
        assert any('import os' in stmt for stmt in import_statements)
    
    def test_complex_code(self):
        """Test parsing of more complex Python code."""
        code = """
import os
from pathlib import Path

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
"""
        result = parse_code_string(code, "python", "test.py")
        
        assert len(result['functions']) >= 2  # process and main
        assert len(result['classes']) == 1
        assert len(result['imports']) >= 2
        assert result['classes'][0]['name'] == 'DataProcessor'


class TestJavaScriptParsing:
    """Test JavaScript code parsing."""
    
    def test_function_extraction(self):
        """Test extraction of JavaScript function."""
        code = """
function add(a, b) {
    return a + b;
}
"""
        result = parse_code_string(code, "javascript", "test.js")
        
        assert len(result['functions']) == 1
        assert result['functions'][0]['name'] == 'add'
        assert result['functions'][0]['parameters'] == ['a', 'b']
    
    def test_class_extraction(self):
        """Test extraction of JavaScript class."""
        code = """
class Rectangle {
    constructor(width, height) {
        this.width = width;
        this.height = height;
    }
}
"""
        result = parse_code_string(code, "javascript", "test.js")
        
        assert len(result['classes']) == 1
        assert result['classes'][0]['name'] == 'Rectangle'
    
    def test_class_with_extends(self):
        """Test extraction of class with extends."""
        code = """
class Square extends Rectangle {
    constructor(side) {
        super(side, side);
    }
}
"""
        result = parse_code_string(code, "javascript", "test.js")
        
        assert len(result['classes']) == 1
        assert result['classes'][0]['name'] == 'Square'


class TestFileParsing:
    """Test file parsing with actual files."""
    
    def test_parse_existing_file(self):
        """Test parsing an actual file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
def test_function():
    return 42
""")
            temp_path = f.name
        
        try:
            result = parse_file(temp_path)
            
            assert result['language'] == 'python'
            assert len(result['functions']) == 1
            assert result['functions'][0]['name'] == 'test_function'
        finally:
            os.unlink(temp_path)
    
    def test_parse_nonexistent_file(self):
        """Test parsing a nonexistent file raises error."""
        with pytest.raises(FileNotFoundError):
            parse_file("/nonexistent/path/file.py")
    
    def test_parse_unsupported_file(self):
        """Test parsing unsupported file type raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xyz', delete=False) as f:
            f.write("some content")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError):
                parse_file(temp_path)
        finally:
            os.unlink(temp_path)


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_code(self):
        """Test parsing empty code."""
        result = parse_code_string("", "python", "test.py")
        
        assert result['language'] == 'python'
        assert len(result['functions']) == 0
        assert len(result['classes']) == 0
        assert len(result['variables']) == 0
    
    def test_code_with_comments_only(self):
        """Test parsing code with only comments."""
        code = """
# This is a comment
# Another comment
"""
        result = parse_code_string(code, "python", "test.py")
        
        assert len(result['functions']) == 0
        assert len(result['classes']) == 0
    
    def test_code_with_syntax_errors(self):
        """Test parsing code with syntax errors (should not crash)."""
        code = """
def incomplete_function(
    # Missing closing parenthesis
"""
        # Should not crash, but may not extract correctly
        result = parse_code_string(code, "python", "test.py")
        
        # Should return a result even with syntax errors
        assert result is not None
        assert result['language'] == 'python'
    
    def test_unicode_characters(self):
        """Test parsing code with unicode characters."""
        code = """
def greet(name):
    message = f"你好, {name}!"
    return message
"""
        result = parse_code_string(code, "python", "test.py")
        
        assert len(result['functions']) == 1
        assert result['functions'][0]['name'] == 'greet'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
