"""
State Explicit
Makes state explicit by identifying and tracking state variables and their mutations.
"""

from typing import Dict, Any, List, Set
from core.csf.schema import generate_node_id


def make_state_explicit(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Make state explicit by identifying state variables and their mutations.
    
    This transformation:
    - Identifies state variables (self.*, class variables, global variables)
    - Tracks state mutations across functions
    - Adds state metadata to nodes for visualization
    
    Args:
        csf: Input CSF structure
        
    Returns:
        CSF with explicit state tracking
    """
    # Identify state variables
    state_variables = identify_state_variables(csf)
    
    # Track state mutations
    state_mutations = track_state_mutations(csf, state_variables)
    
    # Add state metadata to nodes
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            # Add state variables used by this function
            node['meta']['state_variables'] = state_variables.get(node_id, [])
            
            # Add state mutations performed by this function
            node['meta']['state_mutations'] = state_mutations.get(node_id, [])
            
            # Calculate state complexity score
            node['meta']['state_complexity'] = calculate_state_complexity(
                state_variables.get(node_id, []),
                state_mutations.get(node_id, [])
            )
    
    return csf


def identify_state_variables(csf: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Identify state variables used by each function.
    
    Args:
        csf: Input CSF structure
        
    Returns:
        Dictionary mapping node_id to list of state variable names
    """
    state_vars = {}
    
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            # Check if this is a method (has self parameter)
            if node['meta'].get('self_parameter'):
                # Identify self.* attributes as state variables
                func_state_vars = []
                
                # Check dependencies for state references
                for dep_id in node['dependencies']:
                    dep_node = csf['nodes'].get(dep_id)
                    if dep_node:
                        # Look for attribute access patterns in dependencies
                        if 'attribute' in dep_node['meta']:
                            func_state_vars.append(dep_node['meta']['attribute'])
                
                state_vars[node_id] = func_state_vars
            else:
                state_vars[node_id] = []
    
    return state_vars


def track_state_mutations(csf: Dict[str, Any], state_variables: Dict[str, List[str]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Track state mutations performed by each function.
    
    Args:
        csf: Input CSF structure
        state_variables: State variables identified for each function
        
    Returns:
        Dictionary mapping node_id to list of state mutation records
    """
    state_mutations = {}
    
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            mutations = []
            
            # Check mutation_affects for state mutations
            for mutation in node.get('mutation_affects', []):
                if isinstance(mutation, dict):
                    if 'variable' in mutation:
                        mutations.append({
                            'variable': mutation['variable'],
                            'type': mutation.get('type', 'unknown'),
                            'line': mutation.get('line', 0)
                        })
            
            state_mutations[node_id] = mutations
    
    return state_mutations


def calculate_state_complexity(state_vars: List[str], mutations: List[Dict[str, Any]]) -> float:
    """
    Calculate state complexity score based on state variables and mutations.
    
    Args:
        state_vars: List of state variables
        mutations: List of state mutations
        
    Returns:
        Complexity score (0.0 to 1.0, higher is more complex)
    """
    if not state_vars and not mutations:
        return 0.0
    
    # Base complexity from number of state variables
    var_complexity = min(len(state_vars) / 10.0, 0.5)
    
    # Additional complexity from mutations
    mutation_complexity = min(len(mutations) / 10.0, 0.5)
    
    return var_complexity + mutation_complexity


__all__ = ['make_state_explicit']
