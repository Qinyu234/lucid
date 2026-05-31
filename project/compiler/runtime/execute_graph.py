import os

def execute_graph(inputs: dict, meta: dict) -> dict:
    graph_path = inputs.get("graph_path")
    registry_path = inputs.get("registry_path")
    trace_dir = inputs.get("trace_dir")
    
    if graph_path is None:
        raise ValueError("input 'graph_path' is required")
    if registry_path is None:
        raise ValueError("input 'registry_path' is required")
    if trace_dir is None:
        raise ValueError("input 'trace_dir' is required")
    
    # Load graph
    from compiler.loader.load_graph import load_graph
    result = load_graph({"path": graph_path}, {})
    graph = result["graph"]
    
    # Validate graph
    from compiler.passes.pass_runner import run_pipeline
    result = run_pipeline({
        "graph": graph,
        "registry_path": registry_path
    }, {})
    
    if not result["ok"]:
        return {"ok": False, "errors": result["errors"]}
    
    # Start trace
    from compiler.runtime.trace_runtime import start_trace
    result = start_trace({
        "graph_id": graph["id"],
        "trace_dir": trace_dir
    }, {})
    run_id = result["run_id"]
    trace_path = result["trace_path"]
    
    # Load all templates used by nodes
    from compiler.loader.load_template import load_template
    templates = {}
    template_ids = set()
    
    for node_id, node in graph["nodes"].items():
        if node.get("type") == "functional":
            template_id = node.get("template_id")
            if template_id and template_id != "input" and template_id != "output" and template_id not in template_ids:
                template_ids.add(template_id)
                result = load_template({
                    "template_id": template_id,
                    "registry_path": registry_path
                }, {})
                templates[template_id] = result["template"]
    
    # Find root node
    root_id = graph.get("root_id")
    root_node = graph["nodes"].get(root_id)
    
    if root_node is None:
        return {"ok": False, "errors": [f"root node '{root_id}' not found"]}
    
    # Dispatch based on root node kind
    kind = root_node.get("kind")
    
    if kind == "SEQ":
        from compiler.runtime.execute_seq import execute_seq
        result = execute_seq({
            "node": root_node
        }, {
            "graph": graph,
            "templates": templates,
            "context": {
                "run_id": run_id,
                "trace_path": trace_path,
                "registry_path": registry_path
            }
        })
        outputs = result["outputs"]
    elif kind == "BRANCH":
        from compiler.runtime.execute_branch import execute_branch
        result = execute_branch({
            "node": root_node
        }, {
            "graph": graph,
            "templates": templates,
            "context": {
                "run_id": run_id,
                "trace_path": trace_path,
                "registry_path": registry_path
            },
            "resolved_inputs": {}
        })
        outputs = result
    elif kind == "LOOP":
        from compiler.runtime.execute_loop import execute_loop
        result = execute_loop({
            "node": root_node
        }, {
            "graph": graph,
            "templates": templates,
            "context": {
                "run_id": run_id,
                "trace_path": trace_path,
                "registry_path": registry_path
            },
            "node_outputs": {}
        })
        outputs = result["outputs"]
    else:
        return {"ok": False, "errors": [f"root node kind '{kind}' not implemented"]}
    
    return {"ok": True, "run_id": run_id, "outputs": outputs}
