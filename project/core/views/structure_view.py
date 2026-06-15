"""
Structure View for Lucid
Based on ARCHITECTURE.html specification
VIEW 01
「代码长什么样？」
AST + module graph，可 zoom
"""

from typing import Dict, Any, List
from ..graph.builder import CodeGraph


class StructureView:
    """
    Structure View per ARCHITECTURE.html VIEW 01.
    Shows the overall code structure with AST + module graph, zoomable.
    """
    
    def __init__(self, graph: CodeGraph):
        self.graph = graph
    
    def get_function_list(self) -> List[Dict[str, Any]]:
        """Get all functions with their locations."""
        functions = self.graph.get_functions()
        return [
            {
                'name': func.name,
                'line': func.source_ref['line'],
                'column': func.source_ref['column'],
                'parameters': func.meta.get('parameters', []),
            }
            for func in functions
        ]
    
    def get_class_list(self) -> List[Dict[str, Any]]:
        """Get all classes (modules per ARCHITECTURE) with their locations and inheritance."""
        classes = self.graph.get_classes()
        return [
            {
                'name': cls.name,
                'line': cls.source_ref['line'],
                'column': cls.source_ref['column'],
                'base_class': cls.meta.get('base_class'),
            }
            for cls in classes
        ]
    
    def get_variable_list(self) -> List[Dict[str, Any]]:
        """Get all variables (states per ARCHITECTURE) with their locations."""
        variables = self.graph.get_variables()
        return [
            {
                'name': var.name,
                'line': var.source_ref['line'],
                'column': var.source_ref['column'],
                'initial_value': var.meta.get('initial_value'),
            }
            for var in variables
        ]
    
    def get_module_list(self) -> List[Dict[str, Any]]:
        """Get all modules per ARCHITECTURE VIEW 01."""
        modules = self.graph.get_modules()
        return [
            {
                'name': mod.name,
                'file_path': mod.source_ref['file_path'],
            }
            for mod in modules
        ]
    
    def render_structure(self) -> str:
        """
        Render the code structure per ARCHITECTURE VIEW 01.
        AST + module graph, zoomable.
        
        Returns:
            Formatted string showing code structure
        """
        lines = [
            f"Code Structure (VIEW 01): {self.graph.file_path}",
            "=" * 50,
            f"Language: {self.graph.language}",
            "",
        ]
        
        # Modules (per ARCHITECTURE VIEW 01)
        modules = self.get_module_list()
        if modules:
            lines.append(f"Modules ({len(modules)}):")
            for mod in modules:
                lines.append(f"  - {mod['name']} ({mod['file_path']})")
            lines.append("")
        
        # Classes (mapped to MODULE per ARCHITECTURE)
        classes = self.get_class_list()
        if classes:
            lines.append(f"Classes ({len(classes)}):")
            for cls in classes:
                base = f" extends {cls['base_class']}" if cls['base_class'] else ""
                lines.append(f"  - {cls['name']}{base} (line {cls['line']})")
            lines.append("")
        
        # Functions
        functions = self.get_function_list()
        if functions:
            lines.append(f"Functions ({len(functions)}):")
            for func in functions:
                params = ', '.join(func['parameters']) if func['parameters'] else ''
                lines.append(f"  - {func['name']}({params}) (line {func['line']})")
            lines.append("")
        
        # Variables (mapped to STATE per ARCHITECTURE)
        variables = self.get_variable_list()
        if variables:
            lines.append(f"Variables/States ({len(variables)}):")
            for var in variables:
                value = f" = {var['initial_value']}" if var['initial_value'] else ""
                lines.append(f"  - {var['name']}{value} (line {var['line']})")
            lines.append("")
        
        return '\n'.join(lines)
