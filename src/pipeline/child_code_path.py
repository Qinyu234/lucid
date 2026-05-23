import os


def child_code_path(parent_path: str, function_name: str) -> str:
    parent = (parent_path or "").rstrip("/\\")
    fn = function_name or "unnamed"
    return f"{parent}/{fn}" if parent else fn
