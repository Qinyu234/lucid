def child_code_path_util(parent_path: str, function_name: str) -> str:
    parent = (parent_path or "").rstrip("/\\")
    fn = function_name or "unnamed"
    if not parent:
        return fn
    return f"{parent}/{fn}"

