def verify_code(code: str, node: dict) -> tuple:
    import os

    from src.shared.validate.validate_generated_code_util import validate_generated_code_util
    from src.pipeline import repair_node_code_path

    expected = node.get("function_name") or "unnamed"
    children = node.get("children", [])
    if children:
        child_modules = {c.get("function_name") for c in children if c.get("function_name")}
        ok, msg = validate_generated_code_util(code, expected, "init", child_modules=child_modules)
        if not ok:
            return ok, msg
        base = os.path.basename((node.get("code_path") or "").rstrip("/\\"))
        if base and base != expected:
            return False, f"package folder name {base} must match function_name {expected}"
        return True, ""
    repair_node_code_path(node)
    base = os.path.basename((node.get("code_path") or "").rstrip("/\\"))
    if base != expected:
        return False, f"code_path basename {base} must match function_name {expected}"
    return validate_generated_code_util(code, expected, "leaf")
