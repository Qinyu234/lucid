def verify_init_file_imports(tree, init_dir) -> tuple:
    """Imports in interface __init__.py: only from .<direct_child> import <child>; no absolute imports."""
    import ast
    from pathlib import Path

    from src.import_rules.stdlib_roots import stdlib_roots

    init_dir = Path(init_dir)
    allowed: set[str] = set()
    for child in init_dir.iterdir():
        if child.name.startswith(".") or child.name == "__pycache__":
            continue
        if child.is_dir() and (child / "__init__.py").is_file():
            allowed.add(child.name)
        elif child.suffix == ".py" and child.name != "__init__.py":
            allowed.add(child.stem)

    stdlib = stdlib_roots()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if node in tree.body:
                return False, "interface __init__ forbids bare import at module level"
            for alias in node.names:
                top = (alias.name or "").split(".")[0]
                if top not in stdlib:
                    return False, f"interface __init__ forbids import {alias.name!r} (stdlib only inside functions)"
            continue

        if not isinstance(node, ast.ImportFrom):
            continue

        if node.level == 0:
            return (
                False,
                "interface __init__ forbids absolute imports (from src...); "
                "use from .<direct_child> import <child> only",
            )

        if node.level != 1:
            return False, "__init__ cannot import from parent or nested subdirectories"

        if not node.module or "." in node.module:
            return False, f"__init__ nested relative import forbidden: {node.module!r}"

        if node.module not in allowed:
            return False, f"__init__ may only import direct child (one level): {node.module!r}"

        child = node.module
        for alias in node.names:
            if alias.asname:
                return (
                    False,
                    f"__init__ forbids alias: from .{child} import {alias.name} as {alias.asname}",
                )
            if alias.name != child:
                return (
                    False,
                    f"__init__ must use from .{child} import {child}, not {alias.name!r}",
                )

    return True, ""
