import importlib.util
import os
import time
import sys

def execute_seq(inputs: dict, meta: dict) -> dict:
    node = inputs.get("node")
    graph = meta.get("graph")
    templates = meta.get("templates", {})
    context = meta.get("context", {})
    
    if node is None:
        raise ValueError("input 'node' is required")
    if graph is None:
        raise ValueError("meta 'graph' is required")
    
    run_id = context.get("run_id")
    trace_path = context.get("trace_path")
    registry_path = context.get("registry_path")
    
    # Get project root from registry path
    registry_dir = os.path.dirname(registry_path)
    project_root = os.path.dirname(registry_dir)
    
    children = node.get("children", [])
    nodes = graph.get("nodes", {})
    edges = graph.get("edges", {})
    edge_transforms = graph.get("edge_transforms", {})
    
    # Track outputs from previous nodes
    node_outputs = {}
    
    # Execute each child in order
    for child_id in children:
        child_node = nodes.get(child_id)
        if child_node is None:
            raise ValueError(f"child node '{child_id}' not found in graph")
        
        # Build inputs for this child node
        child_inputs = {}
        
        # Find edges that connect to this node
        for edge_id, edge in edges.items():
            if edge.get("to_node") == child_id:
                from_node = edge.get("from_node")
                from_port = edge.get("from_port")
                to_port = edge.get("to_port")
                
                # Get output from previous node
                if from_node in node_outputs:
                    from_node_result = node_outputs[from_node]
                    from_node_outputs = from_node_result.get("outputs", {})
                    value = from_node_outputs.get(from_port)
                    
                    # Apply edge transform if exists
                    if edge_id in edge_transforms:
                        transform = edge_transforms[edge_id]
                        if "wrap" in transform:
                            wrap_config = transform["wrap"]
                            value = {wrap_config.get("key", from_port): value}
                    
                    child_inputs[to_port] = value
        
        # Add params if present
        if "params" in child_node:
            for key, value in child_node["params"].items():
                # Resolve paths relative to project root
                if key == "path" and isinstance(value, str) and not os.path.isabs(value):
                    value = os.path.join(project_root, value)
                child_inputs[key] = value
        
        # Execute the node
        start_time = time.time()
        error = None
        outputs = None
        status = "ok"
        
        try:
            if child_node.get("type") == "control":
                kind = child_node.get("kind")
                if kind == "BRANCH":
                    from compiler.runtime.execute_branch import execute_branch
                    outputs = execute_branch({
                        "node": child_node
                    }, {
                        "graph": graph,
                        "templates": templates,
                        "context": context,
                        "node_outputs": node_outputs
                    })
                elif kind == "LOOP":
                    from compiler.runtime.execute_loop import execute_loop
                    outputs = execute_loop({
                        "node": child_node
                    }, {
                        "graph": graph,
                        "templates": templates,
                        "context": context,
                        "node_outputs": node_outputs
                    })
                else:
                    raise ValueError(f"Control kind '{kind}' not implemented in SEQ")
            else:
                outputs = execute_node(child_node, child_inputs, templates, registry_path)
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
                    "node_id": child_id,
                    "node_inputs": child_inputs,
                    "node_outputs": outputs,
                    "status": status,
                    "error": error,
                    "duration_ms": duration_ms
                }, {})
        
        # Store outputs for next nodes
        node_outputs[child_id] = outputs
    
    # Return outputs of the last node
    last_child_id = children[-1] if children else None
    if last_child_id:
        return node_outputs.get(last_child_id, {})
    
    return {}

def execute_node(node: dict, inputs: dict, templates: dict, registry_path: str) -> dict:
    """Execute a single functional node"""
    node_type = node.get("type")
    
    if node_type == "control":
        # For now, only handle SEQ
        kind = node.get("kind")
        if kind == "SEQ":
            # This shouldn't happen in execute_seq, but handle recursively
            raise ValueError("Nested SEQ not implemented yet")
        else:
            raise ValueError(f"Control kind '{kind}' not implemented")
    
    elif node_type == "functional":
        template_id = node.get("template_id")
        
        # Handle built-in "input" node
        if template_id == "input":
            # Return all params as outputs to their respective ports
            outputs = {}
            for key, value in inputs.items():
                outputs[key] = value
            return {"outputs": outputs}
        
        # Handle built-in "output" node
        if template_id == "output":
            # Pass through the value
            value = inputs.get("value")
            return {"outputs": {"value": value}}
        
        # Load template
        template = templates.get(template_id)
        if template is None:
            raise ValueError(f"Template '{template_id}' not loaded")
        
        # Get implementation
        implementations = template.get("implementations", {})
        python_impl = implementations.get("python", {})
        code_file = python_impl.get("code_file")
        
        if code_file is None:
            raise ValueError(f"No code_file for template '{template_id}'")
        
        # Resolve code file path relative to project root
        registry_dir = os.path.dirname(registry_path)
        project_root = os.path.dirname(registry_dir)
        
        # The code_file is relative to the template's directory
        # We need to find the template location from the registry
        # For now, construct it based on template_id
        template_dir = os.path.join(project_root, "templates", "functional", template_id)
        code_path = os.path.join(template_dir, code_file)
        
        # Load and execute the function
        spec = importlib.util.spec_from_file_location("code_module", code_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find the function (should match template_id)
        func_name = template_id
        if func_name not in dir(module):
            raise ValueError(f"Function '{func_name}' not found in {code_path}")
        
        func = getattr(module, func_name)
        result = func(inputs, {})
        
        # Wrap result in "outputs" key if not already present
        if "outputs" not in result:
            result = {"outputs": result}
        
        return result
    
    else:
        raise ValueError(f"Unknown node type: {node_type}")
