"""
Nesting Flatten
Analyzes and marks deeply nested blocks for potential extraction.
"""

import copy
from typing import Dict, Any

from core.expansion.nesting_depth import calculate_nesting_depths
from core.expansion.nesting_guard import identify_guard_chains


def flatten_nesting(csf: Dict[str, Any], max_depth: int = 3) -> Dict[str, Any]:
    """
    Analyze nesting depth and mark blocks that are too deep.
    
    Args:
        csf: CSF dict to analyze
        max_depth: Maximum allowed nesting depth (default: 3)
        
    Returns:
        Updated CSF dict with nesting annotations (copy, not modifying original)
    """
    # Create a deep copy to avoid modifying original
    csf_analyzed = copy.deepcopy(csf)
    
    # Build ownership tree and calculate depths
    depths = calculate_nesting_depths(csf_analyzed)
    
    # Mark blocks that exceed max_depth
    for node_id, depth in depths.items():
        if node_id not in csf_analyzed['nodes']:
            continue
        
        node = csf_analyzed['nodes'][node_id]
        
        if node['kind'] == 'block' and depth > max_depth:
            node['meta']['nesting_depth'] = depth
            node['meta']['suggest_extraction'] = True
    
    # Identify guard chains
    identify_guard_chains(csf_analyzed)
    
    return csf_analyzed
