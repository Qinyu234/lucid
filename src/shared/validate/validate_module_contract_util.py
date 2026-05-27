def validate_module_contract_util(path) -> list[str]:
    import ast
    from pathlib import Path

    from src.shared.validate.validate_adapter_file_imports_util import (
        validate_adapter_file_imports_util,
    )
    from src.shared.validate.validate_compiler_adapter_stem_util import (
        validate_compiler_adapter_stem_util,
    )
    from src.shared.validate.validate_leaf_file_imports_util import (
        validate_leaf_file_imports_util,
    )
    from src.shared.validate.validate_single_named_function_util import (
        validate_single_named_function_util,
    )

    path = Path(path)
    src_root = path.parent
    while src_root.name != "src" and src_root.parent != src_root:
        src_root = src_root.parent
    if src_root.name != "src":
        src_root = path.parent

    issues: list[str] = []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        return [f"syntax error: {exc}"]

    ok, msg = validate_single_named_function_util(tree, path.stem)
    if not ok:
        issues.append(f"single_function: {msg}")

    is_adapter = validate_compiler_adapter_stem_util(path.stem)
    if is_adapter:
        issues.append(f"role: compiler_adapter (stem {path.stem!r})")
        ok, msg = validate_adapter_file_imports_util(tree, src_root=src_root)
        if not ok:
            issues.append(f"adapter_imports: {msg}")
        ok, msg = validate_leaf_file_imports_util(tree)
        if not ok:
            issues.append(f"leaf_imports_would_fail: {msg}")
    else:
        issues.append("role: leaf")
        ok, msg = validate_leaf_file_imports_util(tree)
        if not ok:
            issues.append(f"leaf_imports: {msg}")

    return issues
