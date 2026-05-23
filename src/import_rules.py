import ast
import sys


def _stdlib_roots() -> set:
    if hasattr(sys, "stdlib_module_names"):
        return set(sys.stdlib_module_names)
    return {
        "os", "sys", "json", "re", "math", "time", "pathlib", "typing",
        "collections", "itertools", "functools", "datetime", "logging",
        "subprocess", "copy", "hashlib", "base64", "io", "abc",
    }


def _top_name(module: str | None) -> str:
    if not module:
        return ""
    return module.split(".")[0]


def verify_single_named_function(tree: ast.AST, expected_name: str) -> tuple:
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    allowed_toplevel = (ast.FunctionDef, ast.Import, ast.ImportFrom)

    for node in tree.body:
        if not isinstance(node, allowed_toplevel):
            return False, "only imports and one function allowed at module level"

    if len(funcs) != 1:
        return False, "exactly one function required"

    if funcs[0].name != expected_name:
        return False, f"function must be named {expected_name}"

    return True, ""


def verify_leaf_imports(tree: ast.AST, shared_root: str = "shared") -> tuple:
    """Leaf: stdlib + shared only; no relative imports."""
    allowed = _stdlib_roots() | {shared_root}

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _top_name(alias.name) not in allowed:
                    return False, f"forbidden import: {alias.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                return False, "relative import not allowed in leaf"
            if _top_name(node.module) not in allowed:
                return False, f"forbidden import from: {node.module}"

    return True, ""


def verify_shared_imports(tree: ast.AST) -> tuple:
    """Shared: stdlib only."""
    allowed = _stdlib_roots()

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _top_name(alias.name) not in allowed:
                    return False, f"shared forbidden import: {alias.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                return False, "relative import not allowed in shared"
            if _top_name(node.module) not in allowed:
                return False, f"shared forbidden import from: {node.module}"

    return True, ""


def verify_init_imports(
    tree: ast.AST,
    child_modules: set,
    shared_root: str = "shared",
) -> tuple:
    """
    __init__: from .<child> import <child> (one level),
              from shared.<m> import <name>
    """
    for node in tree.body:
        if isinstance(node, ast.Import):
            return False, "__init__ forbids bare import"

        if not isinstance(node, ast.ImportFrom):
            continue

        if node.level == 1 and node.module:
            parts = node.module.split(".")
            if len(parts) != 1 or parts[0] not in child_modules:
                return False, f"__init__ child import not allowed: {node.module}"
            continue

        if node.level == 0 and _top_name(node.module) == shared_root:
            continue

        return False, f"__init__ import not allowed: {node.module}"

    return True, ""


def verify_generated_code(
    code: str,
    expected_fn: str,
    kind: str,
    child_modules: set | None = None,
    shared_root: str = "shared",
) -> tuple:
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, str(e)

    ok, msg = verify_single_named_function(tree, expected_fn)
    if not ok:
        return False, msg

    if kind == "leaf":
        return verify_leaf_imports(tree, shared_root)

    if kind == "init":
        return verify_init_imports(tree, child_modules or set(), shared_root)

    if kind == "shared":
        return verify_shared_imports(tree)

    return False, f"unknown kind: {kind}"
