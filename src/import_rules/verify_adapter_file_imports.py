def verify_adapter_file_imports(tree, src_root=None) -> tuple:
    """Adapter: absolute src.* imports must target a package dir or allowed roots.

    Rules (filesystem-backed, no semantic inference):
      - src.shared.*  -> allowed (shared module paths)
      - src.import_rules.<module> -> allowed (compiler import_rules tools)
      - src.<one_part> -> allowed (e.g. src.load_jobs, src.pipeline)
      - src.a.b -> allowed only if src/a/b/__init__.py exists (subpackage)
      - otherwise -> forbidden (must import via parent __init__)
    Relative imports: level 1 only, no dotted module tail.
    """
    import ast
    from pathlib import Path

    from src.import_rules.is_src_shared_module import is_src_shared_module

    root = Path(src_root) if src_root is not None else Path(__file__).resolve().parent.parent

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                msg = _check_src_absolute_module(alias.name or "", root)
                if msg:
                    return False, msg
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                if node.level != 1:
                    return False, f"adapter relative import level must be 1, not {node.level}"
                if node.module and "." in node.module:
                    return False, f"adapter relative import must be one level: {node.module!r}"
                continue
            mod = node.module or ""
            if mod.startswith("src."):
                msg = _check_src_absolute_module(mod, root)
                if msg:
                    return False, msg
    return True, ""


def _check_src_absolute_module(module: str, src_root) -> str | None:
    from src.import_rules.is_src_shared_module import is_src_shared_module

    if not module.startswith("src."):
        return None
    if is_src_shared_module(module, leaf_direct=True) or is_src_shared_module(
        module, leaf_direct=False
    ):
        return None

    rest = module[len("src.") :]
    if not rest:
        return "adapter forbids bare import src"

    parts = rest.split(".")
    if parts[0] == "import_rules" and len(parts) == 2:
        return None

    if len(parts) == 1:
        return None

    pkg_dir = src_root.joinpath(*parts)
    if pkg_dir.is_dir() and (pkg_dir / "__init__.py").is_file():
        return None

    top = parts[0]
    return (
        f"adapter must import via package __init__, not leaf path {module!r}; "
        f"use from src.{top} import <name>"
    )
