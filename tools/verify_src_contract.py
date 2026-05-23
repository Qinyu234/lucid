#!/usr/bin/env python3
"""Verify src/ modules follow codegen-src contract."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

EXEMPT = {
    "errors.py",
    "import_rules.py",
    "schema/engine.py",
}


def _expected_name(path: Path) -> str:
    if path.name == "__init__.py":
        return path.parent.name
    return path.stem


def check_file(path: Path) -> list[str]:
    rel = path.relative_to(SRC).as_posix()
    if rel in EXEMPT:
        return []

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as exc:
        return [f"{rel}: syntax error: {exc}"]

    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    issues = []

    if classes:
        issues.append(f"{rel}: top-level classes forbidden: {[c.name for c in classes]}")

    if path.name == "__init__.py":
        body = [n for n in tree.body if not isinstance(n, (ast.Expr, ast.Import, ast.ImportFrom))]
        if not funcs and not any(isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant) for n in tree.body):
            if any(isinstance(n, ast.ImportFrom) for n in tree.body):
                issues.append(f"{rel}: namespace __init__ must not re-export; import leaf modules directly")
        elif len(funcs) > 1:
            issues.append(f"{rel}: composite __init__ must expose one function, got {[f.name for f in funcs]}")
        elif len(funcs) == 1 and funcs[0].name != _expected_name(path):
            issues.append(f"{rel}: __init__ function must be named {_expected_name(path)}")
        return issues

    if len(funcs) != 1:
        issues.append(f"{rel}: leaf must expose one function, got {[f.name for f in funcs]}")
        return issues

    expected = _expected_name(path)
    if funcs[0].name != expected:
        issues.append(f"{rel}: function must be named {expected}, got {funcs[0].name}")

    return issues


def main() -> int:
    issues: list[str] = []
    for path in sorted(SRC.rglob("*.py")):
        issues.extend(check_file(path))

    if issues:
        print(f"src contract violations: {len(issues)}")
        for item in issues:
            print(f"  - {item}")
        return 1

    print("src contract OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
