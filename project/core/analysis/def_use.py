"""
Def-Use analysis for Lucid
Tracks definition and use relationships for variables
"""

from typing import Dict, Any, List, Set, Tuple
from ..graph.builder import CodeGraph


def analyze_def_use(graph: CodeGraph, source_code: str) -> Dict[str, Any]:
    """
    Perform definition-use analysis on the code graph.
    
    Args:
        graph: CodeGraph from graph layer
        source_code: Raw source code string
        
    Returns:
        Dictionary with def-use information:
        - definitions: variable -> list of definition locations
        - uses: variable -> list of use locations
        - def_use_chains: list of definition->use chains
    """
    lines = source_code.split('\n')
    
    definitions: Dict[str, List[str]] = {}
    uses: Dict[str, List[str]] = {}
    def_use_chains: List[Dict[str, Any]] = []
    
    # Get all variables
    variables = graph.get_variables()
    
    for var_node in variables:
        var_name = var_node.name
        def_loc = f"{graph.file_path}:{var_node.source_ref['line']}"
        
        # Track definitions
        if var_name not in definitions:
            definitions[var_name] = []
        definitions[var_name].append(def_loc)
        
        # Find uses
        var_uses = _find_uses(var_name, lines, graph)
        uses[var_name] = var_uses
        
        # Create def-use chains
        for use_loc in var_uses:
            def_use_chains.append({
                'variable': var_name,
                'definition': def_loc,
                'use': use_loc,
            })
    
    return {
        'definitions': definitions,
        'uses': uses,
        'def_use_chains': def_use_chains,
    }


def _find_uses(var_name: str, lines: List[str], graph: CodeGraph) -> List[str]:
    """Find all use locations for a variable."""
    uses = []
    
    for i, line in enumerate(lines, 1):
        # Simple pattern matching - could be enhanced with AST
        if var_name in line:
            # Skip assignments (writes)
            if f'{var_name} =' not in line and f'{var_name}=' not in line:
                uses.append(f"{graph.file_path}:{i}")
    
    return uses
