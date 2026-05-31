def validate_edges(inputs: dict, meta: dict) -> dict:
    graph = inputs.get("graph")
    
    if graph is None:
        raise ValueError("input 'graph' is required")
    
    errors = []
    nodes = graph.get("nodes", {})
    edges = graph.get("edges", {})
    
    # Validate each edge
    for edge_id, edge in edges.items():
        from_node = edge.get("from_node")
        to_node = edge.get("to_node")
        from_port = edge.get("from_port")
        to_port = edge.get("to_port")
        
        # Check from_node exists
        if from_node not in nodes:
            errors.append(f"edge '{edge_id}': from_node '{from_node}' not found in nodes")
            continue
        
        # Check to_node exists
        if to_node not in nodes:
            errors.append(f"edge '{edge_id}': to_node '{to_node}' not found in nodes")
            continue
        
        # Check from_port exists in from_node's outputs
        from_node_obj = nodes[from_node]
        from_node_outputs = from_node_obj.get("outputs", {})
        if from_port not in from_node_outputs:
            errors.append(f"edge '{edge_id}': from_port '{from_port}' not found in outputs of node '{from_node}'")
        
        # Check to_port exists in to_node's inputs
        to_node_obj = nodes[to_node]
        to_node_inputs = to_node_obj.get("inputs", {})
        if to_port not in to_node_inputs:
            errors.append(f"edge '{edge_id}': to_port '{to_port}' not found in inputs of node '{to_node}'")
    
    return {"graph": graph, "errors": errors}
