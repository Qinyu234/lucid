"""
Access Contract extraction for Lucid
For every piece of state, track who writes it and who reads it
"""

from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, asdict


@dataclass
class WriteSite:
    """Represents a location where a variable is written to."""
    location: str  # e.g., "CartService.addItem:L34"
    line: int
    context: str  # Function/method name
    scope: str = "module"  # Scope level (module, function, class)


@dataclass
class UseSite:
    """Represents a location where a variable is read from."""
    location: str  # e.g., "CartSummary.tsx:L45"
    line: int
    context: str  # Function/method name
    scope: str = "module"  # Scope level (module, function, class)


@dataclass
class AccessContract:
    """
    Access Contract for a piece of state.
    
    Example:
    {
      "cartTotal": {
        "defined": "CartService.ts:12",
        "write_sites": ["CartService.addItem:L34", "CartService.removeItem:L89"],
        "use_sites": ["CartSummary.tsx:L45", "CheckoutButton.tsx:L67"],
        "source": "inferred"
      }
    }
    """
    variable_name: str
    defined: str  # Where it's first defined
    write_sites: List[WriteSite]
    use_sites: List[UseSite]
    source: str = "inferred"  # "inferred" or "explicit"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format matching README example."""
        return {
            self.variable_name: {
                "defined": self.defined,
                "write_sites": [ws.location for ws in self.write_sites],
                "use_sites": [us.location for us in self.use_sites],
                "source": self.source,
            }
        }


def extract_access_contracts(graph, source_code: str, ast=None) -> Dict[str, AccessContract]:
    """
    Extract access contracts for all variables in the code.
    
    Args:
        graph: CodeGraph from graph layer
        source_code: Raw source code string
        ast: Optional tree-sitter AST for more accurate analysis
        
    Returns:
        Dictionary mapping variable names to AccessContract objects
    """
    contracts: Dict[str, AccessContract] = {}
    lines = source_code.split('\n')
    
    # Get all variable nodes
    variables = graph.get_variables()
    
    # Build scope information from AST if available
    scope_info = _build_scope_info(ast, source_code, graph) if ast else {}
    
    for var_node in variables:
        var_name = var_node.name
        defined_location = f"{graph.file_path}:{var_node.source_ref['line']}"
        
        # Find write sites (assignments to this variable)
        write_sites = _find_write_sites(var_name, lines, graph, scope_info)
        
        # Find use sites (reads of this variable)
        use_sites = _find_use_sites(var_name, lines, graph, scope_info)
        
        contracts[var_name] = AccessContract(
            variable_name=var_name,
            defined=defined_location,
            write_sites=write_sites,
            use_sites=use_sites,
            source="inferred"
        )
    
    return contracts


def _build_scope_info(ast, source_code: str, graph) -> Dict[str, Any]:
    """
    Build scope information from AST for accurate variable tracking.
    
    Args:
        ast: Tree-sitter AST
        source_code: Source code string
        graph: CodeGraph
        
    Returns:
        Dictionary with scope information
    """
    scope_info = {
        'scopes': {},  # line -> scope_name
        'variables_in_scope': {},  # scope_name -> set of variable names
    }
    
    if not ast:
        return scope_info
    
    # Track current scope as we traverse
    current_scope = "module"
    scope_stack = ["module"]
    
    def traverse(node, depth=0):
        nonlocal current_scope, scope_stack
        
        node_type = node.type
        line = node.start_point[0] + 1
        
        # Enter new scope for functions/classes
        if node_type in ['function_definition', 'function_declaration', 'method_definition', 'class_definition', 'class_declaration']:
            # Find function/class name
            name = None
            for child in node.children:
                if child.type == 'identifier':
                    name = child.text.decode('utf-8')
                    break
            
            if name:
                scope_stack.append(name)
                current_scope = name
                scope_info['scopes'][line] = current_scope
                if current_scope not in scope_info['variables_in_scope']:
                    scope_info['variables_in_scope'][current_scope] = set()
        
        # Track variable assignments in current scope
        elif node_type in ['assignment', 'assignment_expression']:
            for child in node.children:
                if child.type == 'identifier':
                    var_name = child.text.decode('utf-8')
                    if current_scope not in scope_info['variables_in_scope']:
                        scope_info['variables_in_scope'][current_scope] = set()
                    scope_info['variables_in_scope'][current_scope].add(var_name)
                    break
        
        # Recursively traverse children
        for child in node.children:
            traverse(child, depth + 1)
        
        # Exit scope
        if node_type in ['function_definition', 'function_declaration', 'method_definition', 'class_definition', 'class_declaration']:
            if len(scope_stack) > 1:
                scope_stack.pop()
                current_scope = scope_stack[-1] if scope_stack else "module"
    
    traverse(ast.root_node)
    return scope_info


def _find_write_sites(var_name: str, lines: List[str], graph, scope_info: Dict[str, Any]) -> List[WriteSite]:
    """
    Find all locations where a variable is written to.
    
    Args:
        var_name: Variable name to search for
        lines: Source code lines
        graph: CodeGraph for context
        scope_info: Scope information from AST
        
    Returns:
        List of WriteSite objects
    """
    write_sites = []
    
    # Get all functions to determine context
    functions = graph.get_functions()
    
    for i, line in enumerate(lines, 1):
        # More sophisticated pattern matching for assignment
        # Use regex to ensure word boundaries
        import re
        assignment_patterns = [
            r'\b' + re.escape(var_name) + r'\s*=',
            r'\b' + re.escape(var_name) + r'\s*\+=',
            r'\b' + re.escape(var_name) + r'\s*-=', 
            r'\b' + re.escape(var_name) + r'\s*\*=',
            r'\b' + re.escape(var_name) + r'\s*/=',
            r'\b' + re.escape(var_name) + r'\s*:=',  # Python walrus operator
        ]
        
        is_assignment = any(re.search(pattern, line) for pattern in assignment_patterns)
        
        if is_assignment:
            # Find which function this is in
            context = _find_context(i, functions, lines)
            
            # Determine scope
            scope = scope_info.get('scopes', {}).get(i, "module")
            
            location = f"{graph.file_path}:{i}"
            write_sites.append(WriteSite(location, i, context, scope))
    
    return write_sites


def _find_use_sites(var_name: str, lines: List[str], graph, scope_info: Dict[str, Any]) -> List[UseSite]:
    """
    Find all locations where a variable is read from.
    
    Args:
        var_name: Variable name to search for
        lines: Source code lines
        graph: CodeGraph for context
        scope_info: Scope information from AST
        
    Returns:
        List of UseSite objects
    """
    use_sites = []
    
    # Get all functions to determine context
    functions = graph.get_functions()
    
    for i, line in enumerate(lines, 1):
        # Check if variable is used (but not assigned)
        # More sophisticated check to avoid false positives
        is_assignment = (
            f'{var_name} =' in line or 
            f'{var_name}=' in line or
            f'{var_name} +=' in line or
            f'{var_name} -=' in line or
            f'{var_name} *=' in line or
            f'{var_name} /=' in line or
            f'{var_name} :=' in line
        )
        
        # Check if variable appears in line (as a word, not as substring)
        import re
        word_pattern = r'\b' + re.escape(var_name) + r'\b'
        appears_as_word = re.search(word_pattern, line) is not None
        
        # Skip comment lines
        is_comment = line.strip().startswith('#')
        
        if appears_as_word and not is_assignment and not is_comment:
            # Skip if it's a definition
            if not line.strip().startswith(('def ', 'class ', 'import ', 'from ')):
                # Find which function this is in
                context = _find_context(i, functions, lines)
                
                # Determine scope
                scope = scope_info.get('scopes', {}).get(i, "module")
                
                location = f"{graph.file_path}:{i}"
                use_sites.append(UseSite(location, i, context, scope))
    
    return use_sites


def _find_context(line_num: int, functions: List, lines: List[str]) -> str:
    """
    Find the function context for a given line number.
    
    Args:
        line_num: Line number to find context for
        functions: List of function nodes
        lines: Source code lines
        
    Returns:
        Function name or "module" if not in a function
    """
    # Find the function that contains this line
    for func in functions:
        body_start = func.meta.get('body_start')
        body_end = func.meta.get('body_end')
        
        if body_start and body_end:
            if body_start <= line_num <= body_end:
                return func.name
    
    return "module"
