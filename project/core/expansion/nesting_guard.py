"""
Guard Chain Identification
Identify guard chains (consecutive if blocks without else)
"""

from typing import Dict, Any


def identify_guard_chains(csf: Dict[str, Any]) -> None:
    """
    Identify guard chains (consecutive if blocks without else).
    
    Args:
        csf: CSF dict to modify in place
    """
    # For each function, check if it has consecutive if blocks
    for node_id, node in csf['nodes'].items():
        if node['kind'] != 'function':
            continue
        
        # Get all block children that are 'if' blocks
        if_blocks = []
        for child_id in node['children']:
            if child_id not in csf['nodes']:
                continue
            child = csf['nodes'][child_id]
            if child['kind'] == 'block' and child['label'] == 'if':
                if_blocks.append(child)
        
        # Check for consecutive if blocks (simplified: if there are 2+ if blocks)
        if len(if_blocks) >= 2:
            for if_block in if_blocks:
                if_block['meta']['guard_chain'] = True
