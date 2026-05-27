def verify_leaf_file_imports(tree) -> tuple:
    """Leaf (non-__init__.py): entire file may only import direct src.shared modules."""
    import ast

    from src.import_rules.is_src_shared_module import is_src_shared_module

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not is_src_shared_module(alias.name, leaf_direct=True):
                    return (
                        False,
                        f"leaf may only import direct src.shared modules: {alias.name!r}",
                    )
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                return False, "leaf cannot use relative imports"
            if not is_src_shared_module(node.module, leaf_direct=True):
                return (
                    False,
                    f"leaf may only import direct src.shared modules, not: {node.module!r}",
                )

    return True, ""
