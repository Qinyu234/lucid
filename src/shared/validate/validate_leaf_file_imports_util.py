def validate_leaf_file_imports_util(tree) -> tuple:
    import ast

    from src.shared.validate.validate_is_src_shared_module_util import (
        validate_is_src_shared_module_util,
    )

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not validate_is_src_shared_module_util(alias.name, leaf_direct=True):
                    return (
                        False,
                        f"leaf may only import direct src.shared modules: {alias.name!r}",
                    )
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                return False, "leaf cannot use relative imports"
            if not validate_is_src_shared_module_util(node.module, leaf_direct=True):
                return (
                    False,
                    f"leaf may only import direct src.shared modules, not: {node.module!r}",
                )

    return True, ""
