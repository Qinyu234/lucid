"""
CSF AST Visitor
AST visitor that builds CSF structure from Python source code
"""

import ast
from typing import Dict, List, Any, Optional
from core.csf.schema import empty_csf, make_node, generate_node_id


class CSFVisitor(ast.NodeVisitor):
    """
    AST visitor that builds CSF structure.
    """
    
    def __init__(self, source_path: str, csf: Dict[str, Any]):
        self.source_path = source_path
        self.csf = csf
        self.node_stack: List[Dict[str, Any]] = []  # Stack of parent nodes
        self.current_function: Optional[Dict[str, Any]] = None
        self.current_class: Optional[Dict[str, Any]] = None
        
    def _get_line_range(self, node: ast.AST) -> Dict[str, int]:
        """Get line range for a node."""
        return {
            "path": self.source_path,
            "line_start": getattr(node, 'lineno', 0),
            "line_end": getattr(node, 'end_lineno', getattr(node, 'lineno', 0)),
        }
    
    def _add_node(self, node: Dict[str, Any], is_root: bool = False) -> None:
        """Add a node to CSF and handle parent-child relationships."""
        self.csf['nodes'][node['id']] = node
        
        if is_root:
            self.csf['root_ids'].append(node['id'])
        
        if self.node_stack:
            parent = self.node_stack[-1]
            parent['children'].append(node['id'])
    
    def visit_Module(self, node: ast.Module) -> None:
        """Visit module (root)."""
        module_node = make_node(
            generate_node_id(),
            "module",
            Path(self.source_path).stem,
            self._get_line_range(node)
        )
        self._add_node(module_node, is_root=True)
        self.node_stack.append(module_node)
        
        self.generic_visit(node)
        
        self.node_stack.pop()
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definition."""
        class_node = make_node(
            generate_node_id(),
            "class",
            node.name,
            self._get_line_range(node)
        )
        self._add_node(class_node)
        
        old_class = self.current_class
        self.current_class = class_node
        self.node_stack.append(class_node)
        
        self.generic_visit(node)
        
        self.node_stack.pop()
        self.current_class = old_class
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition."""
        self._visit_function(node, "function")
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definition."""
        self._visit_function(node, "function")
    
    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef, kind: str) -> None:
        """Common function visitor logic."""
        func_node = make_node(
            generate_node_id(),
            kind,
            node.name,
            self._get_line_range(node)
        )
        self._add_node(func_node)
        
        old_function = self.current_function
        self.current_function = func_node
        self.node_stack.append(func_node)
        
        self.generic_visit(node)
        
        self.node_stack.pop()
        self.current_function = old_function
    
    def visit_If(self, node: ast.If) -> None:
        """Visit if statement (block)."""
        self._visit_block(node, "if")
    
    def visit_For(self, node: ast.For) -> None:
        """Visit for loop (block)."""
        self._visit_block(node, "for")
    
    def visit_While(self, node: ast.While) -> None:
        """Visit while loop (block)."""
        self._visit_block(node, "while")
    
    def _visit_block(self, node: ast.AST, label: str) -> None:
        """Common block visitor logic."""
        block_node = make_node(
            generate_node_id(),
            "block",
            label,
            self._get_line_range(node)
        )
        self._add_node(block_node)
        self.node_stack.append(block_node)
        
        self.generic_visit(node)
        
        self.node_stack.pop()
    
    def visit_Assign(self, node: ast.Assign) -> None:
        """Visit assignment statement."""
        stmt_node = make_node(
            generate_node_id(),
            "statement",
            "assign",
            self._get_line_range(node)
        )
        
        # Record mutations (targets)
        for target in node.targets:
            if isinstance(target, ast.Name):
                stmt_node['mutations'].append(target.id)
        
        self._add_node(stmt_node)
        
        # Visit value to find dependencies
        self.visit(node.value)
    
    def visit_Call(self, node: ast.Call) -> None:
        """Visit function call (record dependency)."""
        if self.node_stack:
            parent = self.node_stack[-1]
            if isinstance(node.func, ast.Name):
                parent['dependencies'].append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                # Record attribute access as dependency
                parent['dependencies'].append(node.func.attr)
        
        self.generic_visit(node)
    
    def visit_Name(self, node: ast.Name) -> None:
        """Visit name reference (record dependency)."""
        if self.node_stack and isinstance(node.ctx, ast.Load):
            parent = self.node_stack[-1]
            if node.id not in parent['dependencies']:
                parent['dependencies'].append(node.id)
        
        self.generic_visit(node)
    
    def visit_Expr(self, node: ast.Expr) -> None:
        """Visit expression statement."""
        stmt_node = make_node(
            generate_node_id(),
            "statement",
            "expr",
            self._get_line_range(node)
        )
        self._add_node(stmt_node)
        self.node_stack.append(stmt_node)
        
        self.generic_visit(node)
        
        self.node_stack.pop()
    
    def visit_Return(self, node: ast.Return) -> None:
        """Visit return statement."""
        stmt_node = make_node(
            generate_node_id(),
            "statement",
            "return",
            self._get_line_range(node)
        )
        self._add_node(stmt_node)
        
        if node.value:
            self.visit(node.value)
