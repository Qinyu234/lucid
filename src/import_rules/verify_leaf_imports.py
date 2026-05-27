def verify_leaf_module_imports(tree, shared_root="src.shared") -> tuple:
    """Leaf: module-level imports only src.shared (compiler incremental check)."""
    import ast

    from src.import_rules.is_src_shared_module import is_src_shared_module

    del shared_root

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not is_src_shared_module(alias.name, leaf_direct=True):
                    return False, f"leaf may only import direct src.shared modules: {alias.name!r}"
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                return False, "leaf cannot use relative imports"
            if not is_src_shared_module(node.module, leaf_direct=True):
                return (
                    False,
                    f"leaf may only import direct src.shared modules, not: {node.module!r}",
                )

    return True, ""


def verify_leaf_imports(tree, shared_root="src.shared") -> tuple:
    """Leaf: entire file may only import direct src.shared (user generated projects)."""
    from src.import_rules.verify_leaf_file_imports import verify_leaf_file_imports

    del shared_root
    return verify_leaf_file_imports(tree)
