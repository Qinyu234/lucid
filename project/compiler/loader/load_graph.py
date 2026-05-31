import json

def load_graph(inputs: dict, meta: dict) -> dict:
    path = inputs.get("path")
    
    if path is None:
        raise ValueError("input 'path' is required")
    
    with open(path, "r", encoding="utf-8") as f:
        graph = json.load(f)
    
    # Check required fields
    required_fields = ["id", "version", "root_id", "nodes", "edges"]
    for field in required_fields:
        if field not in graph:
            raise ValueError(f"graph missing required field: {field}")
    
    # Check root_id exists in nodes
    root_id = graph["root_id"]
    if root_id not in graph["nodes"]:
        raise ValueError(f"root_id '{root_id}' not found in nodes")
    
    return {"graph": graph}
