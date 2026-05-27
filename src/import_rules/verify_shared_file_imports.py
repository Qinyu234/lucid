def verify_shared_file_imports(tree) -> tuple:
    """Shared module: entire file may only import stdlib, third-party, or src.shared.*."""
    import ast

    from src.import_rules.is_src_shared_module import is_src_shared_module
    from src.import_rules.stdlib_roots import stdlib_roots

    stdlib = stdlib_roots()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                top = (alias.name or "").split(".")[0]
                if top == "src" and not is_src_shared_module(alias.name):
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
            if not is_src_shared_module(mod):
                return False, f"shared forbidden import from: {mod!r}"
            continue
        if top not in stdlib:
            continue
    return True, ""
