"""
Nesting Depth Calculation
Calculate nesting depth for nodes in the ownership tree
"""

from typing import Dict, Set
from collections import deque


def calculate_nesting_depths(csf: Dict[str, any]) -> Dict[str, int]:
    """
    Calculate nesting depth for each node in the ownership tree.
    
    Args:
        csf: CSF dict
        
    Returns:
        Map of node_id to nesting depth (distance from root)
    """
    depths: Dict[str, int] = {}
    
    # Find root nodes (nodes with no parent in root_ids)
    root_ids = csf['root_ids']
    
    # BFS from roots to calculate depths
    queue = deque()
    visited: Set[str] = set()
    
    for root_id in root_ids:
        if root_id in csf['nodes']:
            queue.append((root_id, 0))
            visited.add(root_id)
    
    while queue:
        node_id, depth = queue.popleft()
        depths[node_id] = depth
        
        if node_id not in csf['nodes']:
            continue
        
        node = csf['nodes'][node_id]
        
        for child_id in node['children']:
            if child_id not in visited and child_id in csf['nodes']:
                visited.add(child_id)
                queue.append((child_id, depth + 1))
    
    return depths
