import time

def execute_loop(inputs: dict, meta: dict) -> dict:
    node = inputs.get("node")
    graph = meta.get("graph")
    templates = meta.get("templates", {})
    context = meta.get("context", {})
    node_outputs = meta.get("node_outputs", {})
    
    if node is None:
        raise ValueError("input 'node' is required")
    if graph is None:
        raise ValueError("meta 'graph' is required")
    
    run_id = context.get("run_id")
    trace_path = context.get("trace_path")
    registry_path = context.get("registry_path")
    
    # Get loop configuration from node
    iterator_port = node.get("iterator_port", "items")
    body = node.get("body")
    accumulator_port = node.get("accumulator_port", "accumulator")
    
    if body is None:
        raise ValueError("node missing 'body' field")
    
    # Resolve inputs from edges
    edges = graph.get("edges", {})
    resolved_inputs = {}
    
    for edge_id, edge in edges.items():
        if edge.get("to_node") == node.get("id"):
            from_node = edge.get("from_node")
            from_port = edge.get("from_port")
            to_port = edge.get("to_port")
            
            if from_node in node_outputs:
                from_node_result = node_outputs[from_node]
                from_node_outputs = from_node_result.get("outputs", {})
                resolved_inputs[to_port] = from_node_outputs.get(from_port)
    
    # Add params if present
    if "params" in node:
        for key, value in node["params"].items():
            resolved_inputs[key] = value
    
    # Get items list
    items = resolved_inputs.get(iterator_port)
    
    if items is None:
        raise ValueError(f"iterator_port '{iterator_port}' not found in inputs")
    if not isinstance(items, list):
        raise TypeError(f"items must be list, got {type(items).__name__}")
    
    # Get initial accumulator
    accumulator = resolved_inputs.get("initial_accumulator", None)
    
    # Iterate
    results = []
    start_time = time.time()
    error = None
    status = "ok"
    
    try:
        for idx, item in enumerate(items):
            # Execute body with item and accumulator
            body_inputs = {
                "item": item,
                "accumulator": accumulator
            }
            
            body_result = execute_body_node(body, graph, templates, registry_path, body_inputs)
            body_outputs = body_result.get("outputs", {})
            
            # Update accumulator
            accumulator = body_outputs.get(accumulator_port, accumulator)
            
            # Collect result (first non-accumulator output)
            for key, value in body_outputs.items():
                if key != accumulator_port:
                    results.append(value)
                    break
            else:
                results.append(None)
    except Exception as e:
        error = str(e)
        status = "error"
        raise
    finally:
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Record trace
        if trace_path and run_id:
            from compiler.runtime.trace_runtime import record_node
            record_node({
                "run_id": run_id,
                "trace_path": trace_path,
                "node_id": node.get("id"),
                "node_inputs": resolved_inputs,
                "node_outputs": {"accumulator": accumulator, "results": results},
                "status": status,
                "error": error,
                "duration_ms": duration_ms
            }, {})
    
    return {"outputs": {"accumulator": accumulator, "results": results}}

def execute_body_node(node_id: str, graph: dict, templates: dict, registry_path: str, inputs: dict) -> dict:
    """Execute the body node"""
    from compiler.runtime.execute_seq import execute_node
    
    node = graph["nodes"].get(node_id)
    if node is None:
        raise ValueError(f"node '{node_id}' not found in graph")
    
    # Add params if present
    if "params" in node:
        for key, value in node["params"].items():
            inputs[key] = value
    
    return execute_node(node, inputs, templates, registry_path)
