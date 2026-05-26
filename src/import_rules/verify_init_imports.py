def verify_init_imports(tree, child_modules, shared_root="src.shared", algorithm_root=None):
    import ast

    from src.import_rules.is_src_shared_module import is_src_shared_module

    del shared_root, algorithm_root

    for node in tree.body:
        if isinstance(node, ast.Import):
            return False, "interface __init__ forbids bare import; use from .<child> or src.shared"

        if not isinstance(node, ast.ImportFrom):
            continue

        if node.level and node.level > 1:
            return False, "__init__ cannot import from parent or nested subdirectories"

        if node.level == 1:
            if not node.module:
                return False, "__init__ use from .<child> import <child>, not from . import ..."
            parts = node.module.split(".")
            if len(parts) != 1 or parts[0] not in child_modules:
                return False, f"__init__ may only import direct child (one level): {node.module}"
            continue

        if node.level == 0:
            if is_src_shared_module(node.module):
                continue
            return False, "only interface __init__ may import non-shared; use from .<child> import <child>"

        return False, f"__init__ import not allowed: {node.module}"

    return True, ""
