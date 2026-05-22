import ast
import os
from pathlib import Path

from src.config import load_app_config
from src.import_rules import (
    verify_init_imports,
    verify_leaf_imports,
    verify_single_run_function,
)


def verify_code(code: str, node: dict) -> tuple:
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, str(e)

    ok, msg = verify_single_run_function(tree)
    if not ok:
        return False, msg

    children = node.get("children", [])
    cfg = load_app_config()
    shared_root = Path(cfg.get("shared_dir", "io/output/shared")).name

    if children:
        child_modules = {
            c.get("function_name") for c in children if c.get("function_name")
        }
        return verify_init_imports(tree, child_modules)

    ok, msg = verify_leaf_imports(tree, shared_root=shared_root)
    if not ok:
        return False, msg

    fn = node.get("function_name") or ""
    if not fn:
        return False, "missing function_name"

    base = os.path.basename((node.get("code_path") or "").rstrip("/\\"))
    if base != fn:
        return False, "code_path basename must match function_name"

    return True, ""
