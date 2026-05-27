def verify_init_imports(tree, child_modules, shared_root="src.shared"):
    import ast

    del shared_root

    for node in tree.body:
        if isinstance(node, ast.Import):
            return False, "interface __init__ forbids bare import; use from .<child> import <child>"

        if not isinstance(node, ast.ImportFrom):
            continue

        if node.level and node.level > 1:
            return False, "__init__ cannot import from parent or nested subdirectories"

        if node.level == 0:
            return (
                False,
                "__init__ may only import direct children in the same directory "
                "(from .<child> import <child>); no absolute or src.shared imports",
            )

        if node.level == 1:
            if not node.module:
                return False, "__init__ use from .<child> import <child>, not from . import ..."
            parts = node.module.split(".")
            if len(parts) != 1 or parts[0] not in child_modules:
                return False, f"__init__ may only import direct child (one level): {node.module}"
            child = parts[0]
            if not node.names:
                return False, f"__init__ from .{child} must import at least one name"
            for alias in node.names:
                name = alias.name
                if alias.asname:
                    return False, f"__init__ forbids import alias: from .{child} import {name} as {alias.asname}"
                if name != child:
                    return False, f"__init__ must use from .{child} import {child}, not {name}"
            continue

        return False, f"__init__ import not allowed: {node.module}"

    return True, ""
