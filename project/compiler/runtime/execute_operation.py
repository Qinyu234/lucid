import json

def execute_operation(inputs: dict, meta: dict) -> dict:
    operation_id = inputs.get("operation_id")
    args = inputs.get("args", [])
    library_path = inputs.get("library_path")
    
    if operation_id is None:
        raise ValueError("input 'operation_id' is required")
    if library_path is None:
        raise ValueError("input 'library_path' is required")
    
    # Load operation library
    with open(library_path, "r", encoding="utf-8") as f:
        library = json.load(f)
    
    # Find operation
    operation = None
    for op in library.get("operations", []):
        if op.get("id") == operation_id:
            operation = op
            break
    
    if operation is None:
        raise ValueError(f"operation '{operation_id}' not found in library")
    
    # Verify args count
    input_shapes = operation.get("input_shapes", [])
    if len(args) != len(input_shapes):
        raise ValueError(f"args count {len(args)} does not match input_shapes count {len(input_shapes)}")
    
    # Bind args to a, b, c
    expr = operation.get("expression", "")
    allowed_builtins = {len, str, int, float, bool, list, dict, set, sorted, sum, min, max, abs, round}
    
    local_vars = {}
    if len(args) > 0:
        local_vars["a"] = args[0]
    if len(args) > 1:
        local_vars["b"] = args[1]
    if len(args) > 2:
        local_vars["c"] = args[2]
    
    # Restricted eval
    result = eval(expr, {"__builtins__": allowed_builtins}, local_vars)
    
    return {"result": result}
