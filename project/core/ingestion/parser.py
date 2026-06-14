"""
Code parser for Lucid ingestion layer
Supports multiple languages using tree-sitter
"""

from pathlib import Path
from typing import Dict, Any, Optional
import tree_sitter


# Language mappings
LANGUAGE_MAP = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.jsx': 'javascript',
    '.go': 'go',
    '.rs': 'rust',
    '.java': 'java',
    '.c': 'c',
    '.cpp': 'cpp',
    '.h': 'c',
    '.hpp': 'cpp',
}


def get_language(file_path: str) -> Optional[str]:
    """
    Determine the language from file extension.
    
    Args:
        file_path: Path to the source file
        
    Returns:
        Language name or None if unsupported
    """
    ext = Path(file_path).suffix.lower()
    return LANGUAGE_MAP.get(ext)


def parse_file(file_path: str) -> Dict[str, Any]:
    """
    Parse a source file and extract its structure.
    
    Args:
        file_path: Path to the source file
        
    Returns:
        Parsed code structure with:
        - language: detected language
        - file_path: original file path
        - source_code: raw source code
        - ast: tree-sitter AST (if available)
        - functions: list of function definitions
        - classes: list of class definitions
        - variables: list of variable assignments
        - imports: list of import statements
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    language = get_language(file_path)
    if language is None:
        raise ValueError(f"Unsupported file type: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    return parse_code_string(source_code, language, file_path)


def parse_code_string(source_code: str, language: str, file_path: str = "<string>") -> Dict[str, Any]:
    """
    Parse source code string and extract its structure.
    
    Args:
        source_code: Source code string
        language: Programming language
        file_path: Original file path (for reference)
        
    Returns:
        Parsed code structure
    """
    result = {
        'language': language,
        'file_path': file_path,
        'source_code': source_code,
        'ast': None,
        'functions': [],
        'classes': [],
        'variables': [],
        'imports': [],
    }
    
    # Try to use tree-sitter if available
    try:
        import tree_sitter_languages as tsl
        
        parser = tree_sitter.Parser()
        parser.set_language(tsl.get_language(language))
        
        tree = parser.parse(bytes(source_code, 'utf8'))
        result['ast'] = tree
        
        # Extract information from AST
        _extract_from_ast(tree, language, result)
        
    except (ImportError, AttributeError):
        # Fallback to basic regex-based parsing if tree-sitter not available
        _extract_basic(source_code, language, result)
    
    return result


def _extract_from_ast(tree: tree_sitter.Tree, language: str, result: Dict[str, Any]) -> None:
    """
    Extract code structure from tree-sitter AST.
    
    Args:
        tree: Tree-sitter AST
        language: Programming language
        result: Result dict to populate
    """
    root_node = tree.root_node
    
    def traverse(node: tree_sitter.Node, depth: int = 0):
        node_type = node.type
        
        # Extract function definitions
        if node_type in ['function_definition', 'function_declaration', 'method_definition']:
            func_info = _extract_function_info(node, language)
            if func_info:
                result['functions'].append(func_info)
        
        # Extract class definitions
        elif node_type in ['class_definition', 'class_declaration']:
            class_info = _extract_class_info(node, language)
            if class_info:
                result['classes'].append(class_info)
        
        # Extract variable assignments
        elif node_type in ['assignment', 'assignment_expression']:
            var_info = _extract_variable_info(node, language)
            if var_info:
                result['variables'].append(var_info)
        
        # Extract imports
        elif node_type in ['import_statement', 'import_from_statement', 'import_declaration']:
            import_info = _extract_import_info(node, language)
            if import_info:
                result['imports'].append(import_info)
        
        # Recursively traverse children
        for child in node.children:
            traverse(child, depth + 1)
    
    traverse(root_node)


def _extract_function_info(node: tree_sitter.Node, language: str) -> Optional[Dict[str, Any]]:
    """Extract function information from AST node."""
    try:
        name_node = None
        params_node = None
        body_node = None
        
        if language == 'python':
            for child in node.children:
                if child.type == 'identifier':
                    name_node = child
                elif child.type == 'parameters':
                    params_node = child
                elif child.type == 'block':
                    body_node = child
        elif language in ['javascript', 'typescript']:
            for child in node.children:
                if child.type == 'identifier':
                    name_node = child
                elif child.type == 'formal_parameters':
                    params_node = child
                elif child.type == 'statement_block':
                    body_node = child
        
        if not name_node:
            return None
        
        return {
            'name': name_node.text.decode('utf-8'),
            'line': node.start_point[0] + 1,
            'column': node.start_point[1],
            'parameters': [p.text.decode('utf-8') for p in params_node.children if p.type == 'identifier'] if params_node else [],
            'body_start': body_node.start_point[0] + 1 if body_node else None,
            'body_end': body_node.end_point[0] + 1 if body_node else None,
        }
    except Exception:
        return None


def _extract_class_info(node: tree_sitter.Node, language: str) -> Optional[Dict[str, Any]]:
    """Extract class information from AST node."""
    try:
        name_node = None
        base_node = None
        
        for child in node.children:
            if child.type == 'identifier':
                if not name_node:
                    name_node = child
                else:
                    base_node = child
            elif child.type == 'superclass' or child.type == 'argument_list':
                base_node = child
        
        if not name_node:
            return None
        
        return {
            'name': name_node.text.decode('utf-8'),
            'line': node.start_point[0] + 1,
            'column': node.start_point[1],
            'base_class': base_node.text.decode('utf-8') if base_node else None,
        }
    except Exception:
        return None


def _extract_variable_info(node: tree_sitter.Node, language: str) -> Optional[Dict[str, Any]]:
    """Extract variable assignment information from AST node."""
    try:
        left_node = None
        right_node = None
        
        for child in node.children:
            if left_node is None and child.type in ['identifier', 'member_expression']:
                left_node = child
            elif child.type not in ['=', ':=']:
                right_node = child
        
        if not left_node:
            return None
        
        var_name = left_node.text.decode('utf-8')
        # Handle member expressions like "self.x"
        if '.' in var_name:
            var_name = var_name.split('.')[-1]
        
        return {
            'name': var_name,
            'line': node.start_point[0] + 1,
            'column': node.start_point[1],
            'value': right_node.text.decode('utf-8') if right_node else None,
        }
    except Exception:
        return None


def _extract_import_info(node: tree_sitter.Node, language: str) -> Optional[Dict[str, Any]]:
    """Extract import information from AST node."""
    try:
        import_text = node.text.decode('utf-8')
        return {
            'statement': import_text,
            'line': node.start_point[0] + 1,
            'column': node.start_point[1],
        }
    except Exception:
        return None


def _extract_basic(source_code: str, language: str, result: Dict[str, Any]) -> None:
    """
    Basic regex-based parsing as fallback.
    This is less accurate than tree-sitter but works without dependencies.
    """
    import re
    
    lines = source_code.split('\n')
    
    if language == 'python':
        # Extract functions
        func_pattern = re.compile(r'^def\s+(\w+)\s*\(([^)]*)\):')
        for i, line in enumerate(lines):
            match = func_pattern.match(line.strip())
            if match:
                result['functions'].append({
                    'name': match.group(1),
                    'line': i + 1,
                    'column': line.find(match.group(1)),
                    'parameters': [p.strip() for p in match.group(2).split(',') if p.strip()],
                })
        
        # Extract classes
        class_pattern = re.compile(r'^class\s+(\w+)(?:\s*\([^)]*\))?:')
        for i, line in enumerate(lines):
            match = class_pattern.match(line.strip())
            if match:
                result['classes'].append({
                    'name': match.group(1),
                    'line': i + 1,
                    'column': line.find(match.group(1)),
                    'base_class': None,
                })
        
        # Extract variable assignments
        var_pattern = re.compile(r'^(\w+)\s*=\s*.+')
        for i, line in enumerate(lines):
            match = var_pattern.match(line.strip())
            if match:
                var_name = match.group(1)
                # Skip keywords
                if var_name not in ['def', 'class', 'import', 'from', 'return', 'if', 'else', 'for', 'while']:
                    result['variables'].append({
                        'name': var_name,
                        'line': i + 1,
                        'column': line.find(var_name),
                        'value': line.split('=', 1)[1].strip() if '=' in line else None,
                    })
        
        # Extract imports
        import_pattern = re.compile(r'^(?:import|from)\s+')
        for i, line in enumerate(lines):
            if import_pattern.match(line.strip()):
                result['imports'].append({
                    'statement': line.strip(),
                    'line': i + 1,
                    'column': 0,
                })
    
    elif language in ['javascript', 'typescript']:
        # Extract functions
        func_pattern = re.compile(r'function\s+(\w+)\s*\(([^)]*)\)')
        for i, line in enumerate(lines):
            match = func_pattern.search(line)
            if match:
                result['functions'].append({
                    'name': match.group(1),
                    'line': i + 1,
                    'column': match.start(1),
                    'parameters': [p.strip() for p in match.group(2).split(',') if p.strip()],
                })
        
        # Extract classes
        class_pattern = re.compile(r'class\s+(\w+)(?:\s+extends\s+(\w+))?')
        for i, line in enumerate(lines):
            match = class_pattern.search(line)
            if match:
                result['classes'].append({
                    'name': match.group(1),
                    'line': i + 1,
                    'column': match.start(1),
                    'base_class': match.group(2),
                })
        
        # Extract imports
        import_pattern = re.compile(r'^(?:import|export)\s+')
        for i, line in enumerate(lines):
            if import_pattern.match(line.strip()):
                result['imports'].append({
                    'statement': line.strip(),
                    'line': i + 1,
                    'column': 0,
                })
