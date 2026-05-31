import json

def validate_nodes(inputs: dict, meta: dict) -> dict:
    graph = inputs.get("graph")
    registry_path = inputs.get("registry_path")
    
    if graph is None:
        raise ValueError("input 'graph' is required")
    if registry_path is None:
        raise ValueError("input 'registry_path' is required")
    
    errors = []
    
    # Load registry
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
    
    # Build set of valid template ids
    valid_template_ids = {tmpl["id"] for tmpl in registry.get("templates", [])}
    
    # Validate each node
    for node_id, node in graph.get("nodes", {}).items():
        node_type = node.get("type")
        
        if node_type == "functional":
            # Check template_id exists
            if "template_id" not in node:
                errors.append(f"node '{node_id}': missing template_id")
            else:
                template_id = node["template_id"]
                # Check template_id in registry
                if template_id not in valid_template_ids:
                    errors.append(f"node '{node_id}': template_id '{template_id}' not in registry")
            
            # Check template_version exists
            if "template_version" not in node:
                errors.append(f"node '{node_id}': missing template_version")
        
        elif node_type == "control":
            # Check kind is valid
            kind = node.get("kind")
            valid_kinds = ["SEQ", "BRANCH", "LOOP", "PARALLEL"]
            if kind not in valid_kinds:
                errors.append(f"node '{node_id}': kind '{kind}' must be one of {valid_kinds}")
        
        else:
            errors.append(f"node '{node_id}': type '{node_type}' must be 'functional' or 'control'")
    
    return {"graph": graph, "errors": errors}
