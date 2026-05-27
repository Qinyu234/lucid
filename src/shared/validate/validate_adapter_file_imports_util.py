def validate_adapter_file_imports_util(tree, src_root=None) -> tuple:
    import ast
    from pathlib import Path

    from src.shared.validate.validate_is_src_shared_module_util import (
        validate_is_src_shared_module_util,
    )

    root = Path(src_root) if src_root is not None else Path(__file__).resolve().parent.parent.parent

    def check_src_absolute_module(module: str) -> str | None:
        if not module.startswith("src."):
            return None
        if validate_is_src_shared_module_util(module, leaf_direct=True) or validate_is_src_shared_module_util(
            module, leaf_direct=False
        ):
            return None

        rest = module[len("src.") :]
        if not rest:
            return "adapter forbids bare import src"

        parts = rest.split(".")
        if len(parts) == 1:
            return None

        pkg_dir = root.joinpath(*parts)
        if pkg_dir.is_dir() and (pkg_dir / "__init__.py").is_file():
            return None

        top = parts[0]
        return (
            f"adapter must import via package __init__, not leaf path {module!r}; "
            f"use from src.{top} import <name>"
        )

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                msg = check_src_absolute_module(alias.name or "")
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
                msg = check_src_absolute_module(mod)
                if msg:
                    return False, msg
    return True, ""
