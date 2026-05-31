def apply_operation(inputs: dict, meta: dict) -> dict:
    graph = inputs.get("graph")
    operation = inputs.get("operation")
    
    if graph is None:
        raise ValueError("input 'graph' is required")
    if operation is None:
        raise ValueError("input 'operation' is required")
    
    op = operation.get("op")
    
    if op == "group_nodes":
        return apply_group_nodes(graph, operation)
    else:
        # Other op types not implemented yet
        return {"graph": graph}

def apply_group_nodes(graph: dict, operation: dict) -> dict:
    node_ids = operation.get("node_ids")
    macro_id = operation.get("macro_id")
    macro_name = operation.get("macro_name")
    
    if node_ids is None:
        raise ValueError("operation missing 'node_ids'")
    if macro_id is None:
        raise ValueError("operation missing 'macro_id'")
    if macro_name is None:
        raise ValueError("operation missing 'macro_name'")
    
    # Validate node_ids exist in graph
    nodes = graph.get("nodes", {})
    for node_id in node_ids:
        if node_id not in nodes:
            raise ValueError(f"node '{node_id}' not found in graph")
    
    # Validate node_ids length >= 2
    if len(node_ids) < 2:
        raise ValueError("node_ids must have at least 2 nodes")
    
    # Find external edges (one endpoint in node_ids, one outside)
    edges = graph.get("edges", {})
    external_edges = {}
    internal_edges = {}
    
    for edge_id, edge in edges.items():
        from_node = edge.get("from_node")
        to_node = edge.get("to_node")
        
        from_in_group = from_node in node_ids
        to_in_group = to_node in node_ids
        
        if from_in_group and to_in_group:
            # Both endpoints in group - internal edge
            internal_edges[edge_id] = edge
        elif from_in_group or to_in_group:
            # One endpoint in group - external edge
            external_edges[edge_id] = edge
    
    # Infer inputs and outputs from external edges
    inputs = {}
    outputs = {}
    
    for edge_id, edge in external_edges.items():
        from_node = edge.get("from_node")
        to_node = edge.get("to_node")
        from_port = edge.get("from_port")
        to_port = edge.get("to_port")
        
        if from_node in node_ids:
            # Edge from group to outside - this is an output
            if from_port not in outputs:
                from_node_def = nodes.get(from_node, {})
                from_node_outputs = from_node_def.get("outputs", {})
                if from_port in from_node_outputs:
                    outputs[from_port] = from_node_outputs[from_port]
        else:
            # Edge from outside to group - this is an input
            if to_port not in inputs:
                to_node_def = nodes.get(to_node, {})
                to_node_inputs = to_node_def.get("inputs", {})
                if to_port in to_node_inputs:
                    inputs[to_port] = to_node_inputs[to_port]
    
    # Create macro node
    macro_node = {
        "id": macro_id,
        "type": "control",
        "kind": "MACRO",
        "name": macro_name,
        "inputs": inputs,
        "outputs": outputs,
        "children": node_ids,
        "internal_edges": internal_edges
    }
    
    # Remove grouped nodes from graph.nodes
    new_nodes = {}
    for node_id, node in nodes.items():
        if node_id not in node_ids:
            new_nodes[node_id] = node
    new_nodes[macro_id] = macro_node
    
    # Update external edges to point to macro node
    new_edges = {}
    for edge_id, edge in edges.items():
        if edge_id in internal_edges:
            # Skip internal edges (they're now in macro_node)
            continue
        
        new_edge = edge.copy()
        from_node = edge.get("from_node")
        to_node = edge.get("to_node")
        
        if from_node in node_ids:
            new_edge["from_node"] = macro_id
        if to_node in node_ids:
            new_edge["to_node"] = macro_id
        
        new_edges[edge_id] = new_edge
    
    # Update graph
    graph["nodes"] = new_nodes
    graph["edges"] = new_edges
    
    return {"graph": graph}
