"""
Inheritance Parser
Parses source code to build class maps for inheritance expansion.
"""

import ast
from pathlib import Path
from typing import Dict, Any


def parse_source_to_ast(source_path: str):
    """Parse source file to AST."""
    try:
        source = Path(source_path).read_text(encoding='utf-8')
        return ast.parse(source, filename=source_path)
    except Exception:
        return None


def build_class_ast_map(tree):
    """Build a map of class name to its AST node."""
    class_ast_map = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_ast_map[node.name] = node
    return class_ast_map


def build_class_csf_map(csf: Dict[str, Any]):
    """Build a map of class name to its CSF node."""
    class_csf_map = {}
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'class':
            class_csf_map[node['label']] = node
    return class_csf_map
