def validate_node_count(inputs: dict, meta: dict) -> dict:
    graph = inputs.get("graph")
    
    if graph is None:
        raise ValueError("input 'graph' is required")
    
    root_id = graph.get("root_id")
    if root_id is None:
        raise ValueError("graph missing 'root_id'")
    
    root_node = graph.get("nodes", {}).get(root_id)
    if root_node is None:
        raise ValueError(f"root node '{root_id}' not found in graph")
    
    # Count direct children of root
    children = root_node.get("children", [])
    node_count = len(children)
    
    errors = []
    warnings = []
    
    if node_count >= 15:
        errors.append(f"节点数为 {node_count}，超过 15 个上限，必须打包后才能执行")
    elif node_count >= 7:
        warnings.append(f"节点数为 {node_count}，建议打包部分节点（>=7 时提示）")
    
    return {"graph": graph, "errors": errors, "warnings": warnings}
