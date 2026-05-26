def verify_leaf_imports(tree, shared_root="src.shared", algorithm_root=None):
    import ast

    from src.import_rules.is_src_shared_module import is_src_shared_module

    del shared_root, algorithm_root

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not is_src_shared_module(alias.name, leaf_direct=True):
                    return False, f"leaf may only import direct src.shared modules: {alias.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                return False, "leaf cannot import subdirectories (relative import forbidden)"
            if not is_src_shared_module(node.module, leaf_direct=True):
                return (
                    False,
                    f"leaf may only import direct src.shared modules, not business packages: {node.module}",
                )

    return True, ""
