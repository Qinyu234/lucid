"""
Skeleton Generator
Generates code skeleton from flowchart representation.
"""

from typing import Dict, Any, List


def generate_skeleton_from_flowchart(flowchart: Dict[str, Any]) -> str:
    """
    Generate code skeleton from flowchart representation.
    
    Args:
        flowchart: Flowchart dictionary with nodes and edges
        
    Returns:
        Generated code skeleton as string
    """
    if not flowchart:
        return "# No flowchart data available\npass"
    
    nodes = flowchart.get('nodes', [])
    edges = flowchart.get('edges', [])
    
    if not nodes:
        return "# No flowchart nodes\npass"
    
    # Generate skeleton based on flowchart structure
    skeleton_lines = []
    
    # Find the entry node (first node or node with type 'entry')
    entry_node = None
    for node in nodes:
        if node.get('type') == 'entry' or node == nodes[0]:
            entry_node = node
            break
    
    if not entry_node:
        entry_node = nodes[0]
    
    # Generate function signature
    func_name = entry_node.get('label', 'generated_function')
    skeleton_lines.append(f"def {func_name}(*args, **kwargs):")
    skeleton_lines.append("    # Generated from flowchart")
    
    # Generate body based on nodes and edges
    body_lines = generate_body_from_nodes(nodes, edges, entry_node)
    skeleton_lines.extend(body_lines)
    
    return "\n".join(skeleton_lines)


def generate_body_from_nodes(nodes: List[Dict], edges: List[Dict], entry_node: Dict) -> List[str]:
    """
    Generate function body from flowchart nodes and edges.
    
    Args:
        nodes: List of flowchart nodes
        edges: List of flowchart edges
        entry_node: The entry node to start from
        
    Returns:
        List of code lines for the function body
    """
    body = []
    indent = "    "
    
    # Build adjacency map
    adj_map = {}
    for edge in edges:
        from_id = edge.get('from')
        to_id = edge.get('to')
        if from_id not in adj_map:
            adj_map[from_id] = []
        adj_map[from_id].append(to_id)
    
    # Simple traversal to generate code
    visited = set()
    current_id = entry_node.get('id')
    
    while current_id and current_id not in visited:
        visited.add(current_id)
        
        # Find current node
        current_node = None
        for node in nodes:
            if node.get('id') == current_id:
                current_node = node
                break
        
        if not current_node:
            break
        
        # Generate code based on node type
        node_type = current_node.get('type', 'function')
        label = current_node.get('label', '')
        
        if node_type == 'condition':
            body.append(f"{indent}if {label}:")
            body.append(f"{indent}{indent}# TODO: implement condition")
            # Get next nodes
            next_ids = adj_map.get(current_id, [])
            if len(next_ids) > 1:
                body.append(f"{indent}else:")
                body.append(f"{indent}{indent}# TODO: implement else branch")
                current_id = next_ids[0]  # Follow first branch
            elif next_ids:
                current_id = next_ids[0]
            else:
                current_id = None
        elif node_type == 'loop':
            body.append(f"{indent}while {label}:")
            body.append(f"{indent}{indent}# TODO: implement loop")
            next_ids = adj_map.get(current_id, [])
            current_id = next_ids[0] if next_ids else None
        elif node_type == 'action':
            body.append(f"{indent}{label}")
            next_ids = adj_map.get(current_id, [])
            current_id = next_ids[0] if next_ids else None
        elif node_type == 'return':
            body.append(f"{indent}return {label}")
            current_id = None
        else:
            body.append(f"{indent}# {node_type}: {label}")
            next_ids = adj_map.get(current_id, [])
            current_id = next_ids[0] if next_ids else None
    
    if not body:
        body.append(f"{indent}pass")
    
    return body


def add_flowchart_metadata(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add flowchart metadata to function nodes.
    
    Args:
        csf: Input CSF structure
        
    Returns:
        CSF with flowchart metadata added to function nodes
    """
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            # Create flowchart structure from function's control flow
            flowchart = build_flowchart_from_function(csf, node_id)
            
            # Add flowchart metadata
            node['meta']['flowchart'] = flowchart
    
    return csf


def build_flowchart_from_function(csf: Dict[str, Any], function_id: str) -> Dict[str, Any]:
    """
    Build flowchart representation from a function node.
    
    Args:
        csf: Input CSF structure
        function_id: ID of the function node
        
    Returns:
        Flowchart dictionary with nodes and edges
    """
    function_node = csf['nodes'].get(function_id)
    if not function_node:
        return {'nodes': [], 'edges': []}
    
    nodes = []
    edges = []
    
    # Add entry node
    entry_id = f"{function_id}_entry"
    nodes.append({
        'id': entry_id,
        'label': 'entry',
        'type': 'entry'
    })
    
    # Add function node
    nodes.append({
        'id': function_id,
        'label': function_node['label'],
        'type': 'function'
    })
    
    # Add edge from entry to function
    edges.append({
        'from': entry_id,
        'to': function_id
    })
    
    # Process children (blocks, statements)
    prev_id = function_id
    for child_id in function_node.get('children', []):
        child_node = csf['nodes'].get(child_id)
        if not child_node:
            continue
        
        child_flow_id = f"{child_id}_flow"
        node_type = child_node['kind']
        
        if node_type == 'block':
            # Control flow block (if, for, while)
            nodes.append({
                'id': child_flow_id,
                'label': child_node['label'],
                'type': 'condition' if child_node['label'] == 'if' else 'loop'
            })
        elif node_type == 'statement':
            # Action statement
            nodes.append({
                'id': child_flow_id,
                'label': child_node['label'],
                'type': 'action'
            })
        else:
            # Other node types
            nodes.append({
                'id': child_flow_id,
                'label': child_node['label'],
                'type': node_type
            })
        
        # Add edge from previous node
        edges.append({
            'from': prev_id,
            'to': child_flow_id
        })
        
        prev_id = child_flow_id
    
    # Add return node if function has return statements
    return_nodes = [cid for cid in function_node.get('children', []) 
                   if csf['nodes'].get(cid, {}).get('label') == 'return']
    if return_nodes:
        return_id = f"{function_id}_return"
        nodes.append({
            'id': return_id,
            'label': 'return',
            'type': 'return'
        })
        edges.append({
            'from': prev_id,
            'to': return_id
        })
    
    return {'nodes': nodes, 'edges': edges}
