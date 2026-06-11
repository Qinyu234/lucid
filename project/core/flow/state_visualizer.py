"""
State Visualizer
Visualizes state flow and state transitions.
"""

from typing import Dict, Any, List


def visualize_state(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate state visualization data from CSF.
    
    Args:
        csf: Input CSF structure with stateflow metadata
        
    Returns:
        Dictionary containing state visualization data
    """
    visualization = {
        'nodes': [],
        'edges': [],
        'state_variables': set()
    }
    
    # Extract state nodes and edges
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            stateflow = node['meta'].get('stateflow', {})
            
            # Add node to visualization
            visualization['nodes'].append({
                'id': node_id,
                'label': node['label'],
                'state_variables': stateflow.get('state_variables', []),
                'state_mutations': stateflow.get('state_mutations', []),
                'state_complexity': stateflow.get('state_complexity', 0.0)
            })
            
            # Collect state variables
            for var in stateflow.get('state_variables', []):
                visualization['state_variables'].add(var)
            
            # Add state transition edges
            for transition in stateflow.get('state_transitions', []):
                visualization['edges'].append({
                    'from': node_id,
                    'to': transition['to_node'],
                    'type': transition.get('type', 'mutation'),
                    'bidirectional': transition.get('bidirectional', False)
                })
    
    visualization['state_variables'] = list(visualization['state_variables'])
    
    return visualization


def generate_state_graph_viz(visualization: Dict[str, Any]) -> str:
    """
    Generate GraphViz DOT format for state visualization.
    
    Args:
        visualization: State visualization data
        
    Returns:
        GraphViz DOT string
    """
    lines = ['digraph StateFlow {']
    lines.append('  rankdir=LR;')
    lines.append('  node [shape=box];')
    
    # Add nodes
    for node in visualization['nodes']:
        label = f"{node['label']}\\nState vars: {len(node['state_variables'])}"
        lines.append(f'  "{node["id"]}" [label="{label}"];')
    
    # Add edges
    for edge in visualization['edges']:
        if edge['bidirectional']:
            lines.append(f'  "{edge["from"]}" <-> "{edge["to"]}";')
        else:
            lines.append(f'  "{edge["from"]}" -> "{edge["to"]}";')
    
    lines.append('}')
    
    return '\n'.join(lines)


__all__ = ['visualize_state', 'generate_state_graph_viz']
