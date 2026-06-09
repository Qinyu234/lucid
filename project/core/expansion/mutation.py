"""
Mutation Propagation Annotation
Tracks which nodes are affected by mutations (assignments) in other nodes.
"""

import copy
from typing import Dict, List, Set, Any


def annotate_mutations(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Annotate mutation propagation: which nodes are affected by each mutation.
    
    Args:
        csf: CSF dict to annotate
        
    Returns:
        Updated CSF dict with mutation_affects annotations (copy, not modifying original)
    """
    # Create a deep copy to avoid modifying original
    csf_annotated = copy.deepcopy(csf)
    
    # Build a map of variable name to nodes that depend on it
    variable_to_dependents: Dict[str, List[str]] = {}
    
    for node_id, node in csf_annotated['nodes'].items():
        for dep in node['dependencies']:
            if dep not in variable_to_dependents:
                variable_to_dependents[dep] = []
            variable_to_dependents[dep].append(node_id)
    
    # For each node with mutations, find affected nodes
    for node_id, node in csf_annotated['nodes'].items():
        if not node['mutations']:
            continue
        
        # Find all nodes that depend on the mutated variables
        affected_nodes: Set[str] = set()
        
        for mutated_var in node['mutations']:
            if mutated_var in variable_to_dependents:
                for dependent_id in variable_to_dependents[mutated_var]:
                    if dependent_id != node_id:  # Don't include self
                        affected_nodes.add(dependent_id)
        
        node['mutation_affects'] = list(affected_nodes)
        
        # Mark high fanout mutations
        if len(affected_nodes) > 5:
            node['meta']['high_fanout_mutation'] = True
    
    return csf_annotated
