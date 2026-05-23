import os

from src.pipeline.child_code_path import child_code_path


def repair_node_code_path(node: dict, parent_path: str | None = None) -> str:

    def _basename(path: str) -> str:
        return os.path.basename((path or "").rstrip("/\\"))

    fn = node.get("function_name") or "unnamed"

    if parent_path is not None:
        node["code_path"] = child_code_path(parent_path, fn)
        return node["code_path"]

    path = (node.get("code_path") or "").strip()
    if not path or _basename(path) != fn:
        parent = os.path.dirname(path.rstrip("/\\")) if path else ""
        node["code_path"] = child_code_path(parent, fn) if parent else fn

    return node["code_path"]
