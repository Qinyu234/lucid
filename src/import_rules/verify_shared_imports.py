def verify_shared_imports(tree):
    import ast

    from src.import_rules.stdlib_roots import stdlib_roots
    from src.import_rules.top_name import top_name

    allowed = stdlib_roots()

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if top_name(alias.name) not in allowed:
                    return False, f"shared forbidden import: {alias.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                return False, "relative import not allowed in shared"
            if top_name(node.module) not in allowed:
                return False, f"shared forbidden import from: {node.module}"

    return True, ""
