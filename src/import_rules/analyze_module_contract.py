"""Programmatic single-module contract report (AST + filesystem rules)."""

from __future__ import annotations

import sys
from pathlib import Path


def analyze_module_contract(path) -> list[str]:
    """Programmatic contract report for one src module (no semantic inference)."""
    import ast

    from src.import_rules.compiler_adapter_stems import is_compiler_adapter_stem
    from src.import_rules.verify_adapter_file_imports import verify_adapter_file_imports
    from src.import_rules.verify_leaf_file_imports import verify_leaf_file_imports
    from src.import_rules.verify_single_named_function import verify_single_named_function

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

    ok, msg = verify_single_named_function(tree, path.stem)
    if not ok:
        issues.append(f"single_function: {msg}")

    is_adapter = is_compiler_adapter_stem(path.stem)
    if is_adapter:
        issues.append(f"role: compiler_adapter (stem {path.stem!r})")
        ok, msg = verify_adapter_file_imports(tree, src_root=src_root)
        if not ok:
            issues.append(f"adapter_imports: {msg}")
        ok, msg = verify_leaf_file_imports(tree)
        if not ok:
            issues.append(f"leaf_imports_would_fail: {msg}")
    else:
        issues.append("role: leaf")
        ok, msg = verify_leaf_file_imports(tree)
        if not ok:
            issues.append(f"leaf_imports: {msg}")

    return issues


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: python -m src.import_rules.analyze_module_contract <path/to/module.py>")
        return 2
    path = Path(argv[0])
    if not path.is_file():
        print(f"file not found: {path}")
        return 2
    for line in analyze_module_contract(path):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
