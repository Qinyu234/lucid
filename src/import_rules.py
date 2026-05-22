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


def verify_leaf_imports(tree: ast.AST, shared_root: str = "shared") -> tuple:
    allowed = _stdlib_roots() | {shared_root}

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                top = _top_name(alias.name)
                if top not in allowed:
                    return False, f"forbidden import: {alias.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                return False, "relative import not allowed in leaf"
            top = _top_name(node.module)
            if top not in allowed:
                return False, f"forbidden import from: {node.module}"

    return True, ""


def verify_init_imports(tree: ast.AST, child_modules: set) -> tuple:
    """Only relative imports from direct children: from .<child> import run"""

    for node in tree.body:
        if isinstance(node, ast.Import):
            return False, "absolute import not allowed in __init__"
        if isinstance(node, ast.ImportFrom):
            if node.level != 1:
                return False, "__init__ may only use from .<child> import"
            if not node.module:
                continue
            parts = node.module.split(".")
            if len(parts) != 1 or parts[0] not in child_modules:
                return False, f"import not in package children: {node.module}"

    return True, ""


def verify_single_run_function(tree: ast.AST) -> tuple:
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    others = [
        n for n in tree.body
        if not isinstance(n, (ast.FunctionDef, ast.Import, ast.ImportFrom))
    ]

    if others:
        return False, "only imports and one function allowed"

    if len(funcs) != 1 or funcs[0].name != "run":
        return False, "exactly one function run() required"

    return True, ""
