"""
Dependency Chain Expansion
Inlines dependency functions within their callers when dependency span is within limits.
"""

import copy
from typing import Dict, List, Any
from core.csf.schema import generate_node_id
from core.expansion.dependency_graph import build_dependency_graph, calculate_dependency_span
from core.expansion.dependency_inliner import inline_dependency


def expand_dependencies(csf: Dict[str, Any], max_span: int = 2) -> Dict[str, Any]:
    """
    Expand dependency chains by inlining called functions.
    
    Args:
        csf: CSF dict to expand
        max_span: Maximum dependency chain depth to auto-inline (default: 2)
        
    Returns:
        Updated CSF dict with inlined dependency nodes (copy, not modifying original)
    """
    # Create a deep copy to avoid modifying original
    csf_expanded = copy.deepcopy(csf)
    
    # Build a map of function name to node IDs
    function_name_to_ids: Dict[str, List[str]] = {}
    for node_id, node in csf_expanded['nodes'].items():
        if node['kind'] == 'function':
            name = node['label']
            if name not in function_name_to_ids:
                function_name_to_ids[name] = []
            function_name_to_ids[name].append(node_id)
    
    # Build dependency graph and calculate spans
    dependency_graph = build_dependency_graph(csf_expanded, function_name_to_ids)
    
    # Process each function node
    for node_id, node in list(csf_expanded['nodes'].items()):
        if node['kind'] != 'function':
            continue
        
        # Get dependencies for this function
        deps = node['dependencies']
        
        for dep_name in deps:
            if dep_name not in function_name_to_ids:
                # External dependency, skip
                continue
            
            # Calculate dependency span for this chain
            span = calculate_dependency_span(node_id, dep_name, dependency_graph, function_name_to_ids, max_depth=10)
            
            if span <= max_span:
                # Inline the dependency function
                for dep_node_id in function_name_to_ids[dep_name]:
                    if dep_node_id in csf_expanded['nodes']:
                        dep_node = csf_expanded['nodes'][dep_node_id]
                        inline_dependency(csf_expanded, node, dep_node, dep_node_id)
            else:
                # Mark as warning
                node['meta']['dependency_span_warning'] = True
    
    return csf_expanded
