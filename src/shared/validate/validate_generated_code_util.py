def validate_generated_code_util(
    code: str,
    expected_fn: str,
    kind: str,
    child_modules: set | None = None,
    shared_root: str = "shared",
) -> tuple:
    import ast

    from src.shared.validate.validate_init_imports_util import validate_init_imports_util
    from src.shared.validate.validate_leaf_imports_util import validate_leaf_imports_util
    from src.shared.validate.validate_shared_imports_util import validate_shared_imports_util
    from src.shared.validate.validate_single_named_function_util import (
        validate_single_named_function_util,
    )

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, str(e)
    ok, msg = validate_single_named_function_util(tree, expected_fn)
    if not ok:
        return False, msg
    if kind == "leaf":
        return validate_leaf_imports_util(tree, shared_root)
    if kind == "init":
        return validate_init_imports_util(tree, child_modules or set(), shared_root)
    if kind == "shared":
        return validate_shared_imports_util(tree)
    return False, f"unknown kind: {kind}"
