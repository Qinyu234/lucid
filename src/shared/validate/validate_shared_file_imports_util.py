def validate_shared_file_imports_util(tree) -> tuple:
    import ast

    from src.shared.validate.validate_is_src_shared_module_util import (
        validate_is_src_shared_module_util,
    )
    from src.shared.validate.validate_stdlib_roots_util import validate_stdlib_roots_util

    stdlib = validate_stdlib_roots_util()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                top = (alias.name or "").split(".")[0]
                if top == "src" and not validate_is_src_shared_module_util(alias.name):
                    return False, f"shared forbidden import: {alias.name!r}"
                continue
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.level and node.level > 0:
            return False, "relative import not allowed in shared"
        mod = node.module or ""
        if not mod:
            continue
        top = mod.split(".")[0]
        if top == "src":
            if not validate_is_src_shared_module_util(mod):
                return False, f"shared forbidden import from: {mod!r}"
            continue
        if top not in stdlib:
            continue
    return True, ""
