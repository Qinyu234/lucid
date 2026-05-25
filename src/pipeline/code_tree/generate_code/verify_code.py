import os
from pathlib import Path

from src.config.load_app_config import load_app_config
from src.import_rules import verify_generated_code
from src.pipeline.repair_node_code_path import repair_node_code_path


def verify_code(code: str, node: dict) -> tuple:

    def _expected_fn(node: dict) -> str:
        return node.get("function_name") or "unnamed"

    def _shared_root() -> str:
        cfg = load_app_config()
        return Path(cfg.get("shared_dir", "io/output/shared")).name

    def _algorithm_root() -> str:
        cfg = load_app_config()
        return Path(cfg.get("algorithm_dir", "io/output/algorithm")).name

    expected = _expected_fn(node)
    children = node.get("children", [])
    shared = _shared_root()
    algorithm = _algorithm_root()

    if children:
        child_modules = {c.get("function_name") for c in children if c.get("function_name")}
        ok, msg = verify_generated_code(
            code,
            expected,
            "init",
            child_modules=child_modules,
            shared_root=shared,
            algorithm_root=algorithm,
        )
        if not ok:
            return ok, msg
        base = os.path.basename((node.get("code_path") or "").rstrip("/\\"))
        if base and base != expected:
            return False, f"package folder name {base} must match function_name {expected}"
        return True, ""

    repair_node_code_path(node)
    base = os.path.basename((node.get("code_path") or "").rstrip("/\\"))
    if base != expected:
        return False, f"code_path basename {base} must match function_name {expected}"

    return verify_generated_code(code, expected, "leaf", shared_root=shared, algorithm_root=algorithm)
