"""
Stateflow Analysis
Analyzes state flow through the code to understand state transitions.
"""

from typing import Dict, Any, List, Set


def analyze_stateflow(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze state flow through the CSF.
    
    Args:
        csf: Input CSF structure
        
    Returns:
        CSF with stateflow metadata added to nodes
    """
    # Build state transition graph
    state_graph = build_state_graph(csf)
    
    # Calculate state transitions
    state_transitions = calculate_state_transitions(state_graph)
    
    # Add stateflow metadata to nodes
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            states = extract_states(node)
            transitions = state_transitions.get(node_id, [])
            node['meta']['stateflow'] = {
                'state_variables': node['meta'].get('state_variables', []),
                'state_mutations': node['meta'].get('state_mutations', []),
                'state_transitions': transitions,
                'state_complexity': node['meta'].get('state_complexity', 0.0),
                'states': states,
                'transitions': transitions,
                'settings': {
                    'track_state_changes': True,
                    'detect_deadlocks': True,
                    'max_states': 100
                }
            }
    
    return csf


def build_state_graph(csf: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Build a graph of state transitions between nodes.
    
    Args:
        csf: Input CSF structure
        
    Returns:
        Dictionary mapping node_id to list of node_ids that transition state
    """
    state_graph = {}
    
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            # State transitions come from mutation_affects
            state_transitions = []
            for mutation in node.get('mutation_affects', []):
                if isinstance(mutation, dict):
                    affected_node = mutation.get('node_id')
                    if affected_node:
                        state_transitions.append(affected_node)
            state_graph[node_id] = state_transitions
    
    return state_graph


def calculate_state_transitions(state_graph: Dict[str, List[str]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Calculate detailed state transitions.
    
    Args:
        state_graph: State transition graph
        
    Returns:
        Dictionary mapping node_id to list of state transition records
    """
    transitions = {}
    
    for node_id, affected_nodes in state_graph.items():
        transition_records = []
        for affected_id in affected_nodes:
            transition_records.append({
                'to_node': affected_id,
                'type': 'mutation',
                'bidirectional': False
            })
        transitions[node_id] = transition_records
    
    return transitions


def extract_states(node: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract state information from a function node.
    
    Args:
        node: Function node
        
    Returns:
        List of state information
    """
    states = []
    
    # Extract from state variables
    for var in node['meta'].get('state_variables', []):
        states.append({
            'name': var,
            'type': 'variable'
        })
    
    # Extract from mutations as potential state changes
    for mutation in node['meta'].get('state_mutations', []):
        if isinstance(mutation, dict):
            states.append({
                'name': mutation.get('name', 'unknown'),
                'type': 'mutation'
            })
        elif isinstance(mutation, str):
            states.append({
                'name': mutation,
                'type': 'mutation'
            })
    
    return states


__all__ = ['analyze_stateflow']
