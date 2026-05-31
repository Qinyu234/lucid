import importlib.util
import os

def run_pipeline(inputs: dict, meta: dict) -> dict:
    graph = inputs.get("graph")
    registry_path = inputs.get("registry_path")
    until = inputs.get("until", "full")
    
    if graph is None:
        raise ValueError("input 'graph' is required")
    if registry_path is None:
        raise ValueError("input 'registry_path' is required")
    
    # Get the directory of this file to locate pass modules
    passes_dir = os.path.dirname(__file__)
    
    # Load validate_nodes pass
    validate_nodes_path = os.path.join(passes_dir, "001_validate_nodes.py")
    spec = importlib.util.spec_from_file_location("validate_nodes", validate_nodes_path)
    validate_nodes_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validate_nodes_module)
    
    # Run validate_nodes
    result = validate_nodes_module.validate_nodes({
        "graph": graph,
        "registry_path": registry_path
    }, {})
    
    if result["errors"]:
        return {"ok": False, "errors": result["errors"], "graph": graph}
    
    if until == "validate":
        return {"ok": True, "errors": [], "graph": graph}
    
    # Load validate_edges pass
    validate_edges_path = os.path.join(passes_dir, "002_validate_edges.py")
    spec = importlib.util.spec_from_file_location("validate_edges", validate_edges_path)
    validate_edges_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validate_edges_module)
    
    # Run validate_edges
    result = validate_edges_module.validate_edges({
        "graph": graph
    }, {})
    
    if result["errors"]:
        return {"ok": False, "errors": result["errors"], "graph": graph}
    
    # Load validate_node_count pass
    validate_node_count_path = os.path.join(passes_dir, "003_validate_node_count.py")
    spec = importlib.util.spec_from_file_location("validate_node_count", validate_node_count_path)
    validate_node_count_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validate_node_count_module)
    
    # Run validate_node_count
    result = validate_node_count_module.validate_node_count({
        "graph": graph
    }, {})
    
    # Print warnings but don't interrupt execution
    if result.get("warnings"):
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
    
    if result["errors"]:
        return {"ok": False, "errors": result["errors"], "graph": graph}
    
    return {"ok": True, "errors": [], "graph": graph}
