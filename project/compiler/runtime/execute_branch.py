import importlib.util
import os
import time

def execute_branch(inputs: dict, meta: dict) -> dict:
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
    
    # Get branch configuration from node
    condition_port = node.get("condition_port", "condition")
    true_branch = node.get("true_branch")
    false_branch = node.get("false_branch")
    
    if true_branch is None:
        raise ValueError("node missing 'true_branch' field")
    
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
    
    # Get condition value
    condition = resolved_inputs.get(condition_port)
    
    if not isinstance(condition, bool):
        raise TypeError(f"condition must be bool, got {type(condition).__name__}")
    
    # Execute the appropriate branch
    start_time = time.time()
    error = None
    result = None
    status = "ok"
    branch_taken = None
    
    try:
        if condition:
            branch_taken = "true_branch"
            result = execute_child_node(true_branch, graph, templates, registry_path, resolved_inputs, node_outputs)
        else:
            if false_branch:
                branch_taken = "false_branch"
                result = execute_child_node(false_branch, graph, templates, registry_path, resolved_inputs, node_outputs)
            else:
                branch_taken = "none"
                result = {"outputs": {"result": None}}
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
                "node_outputs": result,
                "status": status,
                "error": error,
                "duration_ms": duration_ms
            }, {})
    
    # Return result in the correct format for branch template
    outputs = result.get("outputs", result)
    return {"outputs": {"result": outputs}}

def execute_child_node(node_id: str, graph: dict, templates: dict, registry_path: str, inputs: dict, parent_outputs: dict) -> dict:
    """Execute a single child node"""
    from compiler.runtime.execute_seq import execute_node
    
    node = graph["nodes"].get(node_id)
    if node is None:
        raise ValueError(f"node '{node_id}' not found in graph")
    
    # Resolve inputs for this child node from edges
    edges = graph.get("edges", {})
    child_inputs = {}
    
    # Copy direct inputs (this includes 'value' from branch inputs)
    child_inputs.update(inputs)
    
    # If the child is parse_text and we have 'value', map it to 'text'
    if node.get("template_id") == "parse_text" and "value" in inputs:
        child_inputs["text"] = inputs["value"]
    
    # Resolve from edges
    for edge_id, edge in edges.items():
        if edge.get("to_node") == node_id:
            from_node = edge.get("from_node")
            from_port = edge.get("from_port")
            to_port = edge.get("to_port")
            
            if from_node in parent_outputs:
                from_node_result = parent_outputs[from_node]
                from_node_outputs = from_node_result.get("outputs", {})
                child_inputs[to_port] = from_node_outputs.get(from_port)
    
    # Add params if present
    if "params" in node:
        for key, value in node["params"].items():
            child_inputs[key] = value
    
    return execute_node(node, child_inputs, templates, registry_path)
