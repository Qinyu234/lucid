from pathlib import Path

from src.config.load_app_config import load_app_config
from src.pipeline.find_parent import find_parent
from src.schema.io.format_io_comment import format_io_comment
from src.schema.io.format_io_side import format_io_side
from src.schema.io.normalize_io import normalize_io


def context_builder(node: dict, root: dict | None = None):

    io = normalize_io(node.get("io"))
    io_in_str, io_out_str = format_io_comment(io)

    parent = find_parent(root, node) if root else None
    fn = node.get("function_name") or "module"

    used_by = []
    imports_from_template = []

    if parent:
        parent_fn = parent.get("function_name") or "package"
        used_by.append(
            f"{parent_fn}/__init__.py imports: from .{fn} import {fn}"
        )
        imports_from_template.append(f"from .{fn} import {fn}")

    cfg = load_app_config()
    shared = Path(cfg.get("shared_dir", "io/output/shared")).name

    return {
        "semantic": node.get("semantic", ""),
        "function_name": fn,
        "io_in": io_in_str,
        "io_out": io_out_str,
        "io_in_fields": io.get("in", []),
        "io_out_fields": io.get("out", []),
        "parent_semantic": (parent or {}).get("semantic", ""),
        "parent_function": (parent or {}).get("function_name", ""),
        "parent_topology": (parent or {}).get("topology"),
        "parent_io_in": format_io_side(((parent or {}).get("io") or {}), "in"),
        "parent_io_out": format_io_side(((parent or {}).get("io") or {}), "out"),
        "used_by": used_by,
        "imports_from_template": imports_from_template,
        "shared_module_prefix": shared,
        "allowed_imports": [f"stdlib", f"{shared}.<module>"],
    }
