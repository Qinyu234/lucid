def validate_single_named_function_util(tree, expected_name):
    import ast

    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    allowed_toplevel = (ast.FunctionDef, ast.Import, ast.ImportFrom)

    for node in tree.body:
        if not isinstance(node, allowed_toplevel):
            return False, "only imports and one function allowed at module level"

    if len(funcs) != 1:
        return False, "exactly one function required"

    if funcs[0].name != expected_name:
        return False, f"function must be named {expected_name}"

    return True, ""
