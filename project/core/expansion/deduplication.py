"""
Function Deduplication
Detects and deduplicates duplicate functions, tracks function reuse.
Supports multiple rounds of deduplication and function duplication for reuse.
"""

from typing import Dict, Any, List, Tuple, Set
from core.csf.schema import generate_node_id


def deduplicate_functions(csf: Dict[str, Any], max_rounds: int = 3) -> Dict[str, Any]:
    """
    Detect and deduplicate duplicate functions in the CSF.
    Supports multiple rounds of deduplication to catch transitive duplicates.
    
    Args:
        csf: Input CSF structure
        max_rounds: Maximum number of deduplication rounds
        
    Returns:
        CSF with duplicate functions removed and reuse tracking added
    """
    previous_count = len(csf['nodes'])
    
    for round_num in range(max_rounds):
        # Group functions by their label (simple deduplication)
        function_groups: Dict[str, List[str]] = {}
        
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                label = node['label']
                if label not in function_groups:
                    function_groups[label] = []
                function_groups[label].append(node_id)
        
        # Track which functions to keep and which to remove
        to_remove = set()
        to_keep = {}
        
        for label, node_ids in function_groups.items():
            if len(node_ids) > 1:
                # Found duplicates - keep the first one, mark others for removal
                to_keep[label] = node_ids[0]
                for dup_id in node_ids[1:]:
                    to_remove.add(dup_id)
            else:
                to_keep[label] = node_ids[0]
        
        # If no duplicates found, stop early
        if not to_remove:
            break
        
        # Remove duplicate nodes
        new_nodes = {}
        for node_id, node in csf['nodes'].items():
            if node_id not in to_remove:
                new_nodes[node_id] = node
        
        # Update references (dependencies, children)
        for node in new_nodes.values():
            # Update dependencies - replace removed IDs with kept IDs
            new_deps = []
            for dep_id in node.get('dependencies', []):
                if dep_id in to_remove:
                    # Find which label group this belongs to and replace with kept ID
                    for label, kept_id in to_keep.items():
                        if dep_id in function_groups.get(label, []):
                            new_deps.append(kept_id)
                            break
                else:
                    new_deps.append(dep_id)
            node['dependencies'] = new_deps
            
            # Update children
            new_children = []
            for child_id in node.get('children', []):
                if child_id not in to_remove:
                    new_children.append(child_id)
            node['children'] = new_children
        
        # Update root_ids
        new_root_ids = [rid for rid in csf['root_ids'] if rid not in to_remove]
        
        csf['nodes'] = new_nodes
        csf['root_ids'] = new_root_ids
        
        # Check if we made progress
        current_count = len(csf['nodes'])
        if current_count == previous_count:
            break
        previous_count = current_count
    
    return csf


def track_function_reuse(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Track how many times each function is used across the codebase.
    
    Args:
        csf: Input CSF structure
        
    Returns:
        CSF with reuse_count metadata added to function nodes
    """
    # Count function references
    reuse_counts: Dict[str, int] = {}
    
    # Initialize counts
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            reuse_counts[node_id] = 0
    
    # Build mapping from function names to node IDs
    name_to_ids: Dict[str, List[str]] = {}
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            name = node['label']
            if name not in name_to_ids:
                name_to_ids[name] = []
            name_to_ids[name].append(node_id)
    
    # Count dependencies (function calls) by name
    for node_id, node in csf['nodes'].items():
        for dep_name in node.get('dependencies', []):
            if dep_name in name_to_ids:
                for dep_id in name_to_ids[dep_name]:
                    if dep_id in reuse_counts:
                        reuse_counts[dep_id] += 1
    
    # Add reuse_count metadata
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            if 'reuse_count' not in node['meta']:
                node['meta']['reuse_count'] = reuse_counts.get(node_id, 0)
    
    return csf


def duplicate_function(
    csf: Dict[str, Any],
    source_node_id: str,
    new_name: str,
    target_parent_id: str = None
) -> str:
    """
    Duplicate a function for intentional reuse.
    Creates a new function node with the same structure but a different name.
    
    Args:
        csf: Input CSF structure to modify
        source_node_id: ID of the function node to duplicate
        new_name: Name for the duplicated function
        target_parent_id: Optional parent node ID to attach the duplicate to
        
    Returns:
        ID of the newly created function node
    """
    if source_node_id not in csf['nodes']:
        raise ValueError(f"Source node {source_node_id} not found in CSF")
    
    source_node = csf['nodes'][source_node_id]
    
    if source_node['kind'] != 'function':
        raise ValueError(f"Source node {source_node_id} is not a function")
    
    # Create new function node
    import copy
    new_node_id = generate_node_id()
    new_node = copy.deepcopy(source_node)
    new_node['id'] = new_node_id
    new_node['label'] = new_name
    new_node['meta']['duplicated_from'] = source_node_id
    new_node['meta']['virtual'] = False  # This is a real duplicate, not virtual
    
    # Add to CSF
    csf['nodes'][new_node_id] = new_node
    
    # If target parent is specified, add as child
    if target_parent_id and target_parent_id in csf['nodes']:
        csf['nodes'][target_parent_id]['children'].append(new_node_id)
    else:
        # Add to root_ids
        csf['root_ids'].append(new_node_id)
    
    return new_node_id


def get_reuse_candidates(csf: Dict[str, Any], min_reuse_count: int = 2) -> List[Dict[str, Any]]:
    """
    Get functions that are reused multiple times and could be candidates for
    further optimization or duplication.
    
    Args:
        csf: Input CSF structure
        min_reuse_count: Minimum reuse count to consider a function as a candidate
        
    Returns:
        List of function nodes with their reuse information
    """
    # First ensure reuse counts are tracked
    csf = track_function_reuse(csf)
    
    candidates = []
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            reuse_count = node['meta'].get('reuse_count', 0)
            if reuse_count >= min_reuse_count:
                candidates.append({
                    'node_id': node_id,
                    'label': node['label'],
                    'reuse_count': reuse_count,
                    'node': node
                })
    
    # Sort by reuse count (most reused first)
    candidates.sort(key=lambda x: x['reuse_count'], reverse=True)
    
    return candidates
