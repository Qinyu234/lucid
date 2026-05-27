"""Verify compiler `src/` against codegen-src contract."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

_SKIP_FILES = frozenset({"verify_src_contract.py", "verify_workplace_contract.py"})
_SKIP_PREFIXES = ("import_rules/verify_",)
_TOP_LEVEL_EXEMPT = frozenset({"verify_src_contract", "verify_workplace_contract"})
_INTERNAL_PACKAGES = frozenset({"import_rules"})
_SHARED_CATEGORY_DIRS = frozenset({"lib", "logging", "validate", "io_tree"})


def _repo_src() -> Path:
    return Path(__file__).resolve().parent


def _init_imported_stems(init_path: Path) -> set[str]:
    tree = ast.parse(init_path.read_text(encoding="utf-8"), filename=str(init_path))
    imported: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
            imported.add(node.module.split(".")[0])
    return imported


def _verify_top_level_exports(src_root: Path) -> list[str]:
    init_path = src_root / "__init__.py"
    if not init_path.is_file():
        return ["src/__init__.py: missing"]
    imported = _init_imported_stems(init_path)
    issues: list[str] = []
    for py in src_root.glob("*.py"):
        stem = py.stem
        if stem == "__init__" or stem in _TOP_LEVEL_EXEMPT:
            continue
        if stem == "import_rules":
            continue
        if stem not in imported:
            issues.append(
                f"src/__init__.py: top-level module {stem!r} not imported "
                f"(every src/*.py must be exported via from .{stem} import {stem})"
            )
    return issues


def _verify_subpackage_exports(src_root: Path) -> list[str]:
    issues: list[str] = []
    for init_path in sorted(src_root.rglob("__init__.py")):
        if "import_rules" in init_path.parts:
            continue
        parent = init_path.parent
        rel_s = init_path.relative_to(src_root).as_posix()
        if parent == src_root / "shared" and rel_s == "shared/__init__.py":
            continue
        if len(parent.relative_to(src_root).parts) >= 2:
            if parent.name in _SHARED_CATEGORY_DIRS and parent.parent.name == "shared":
                continue
        imported = _init_imported_stems(init_path)
        for child in parent.iterdir():
            if not child.is_dir() or child.name.startswith(".") or child.name == "__pycache__":
                continue
            if not (child / "__init__.py").is_file():
                continue
            if child.name not in imported:
                if parent == src_root and child.name in _INTERNAL_PACKAGES:
                    continue
                issues.append(
                    f"{rel_s}: missing subpackage import .{child.name} "
                    f"(direct child package must be from .{child.name} import {child.name})"
                )
    return issues


def _direct_child_stems(init_dir: Path) -> set[str]:
    stems: set[str] = set()
    if not init_dir.is_dir():
        return stems
    for child in init_dir.iterdir():
        if child.name.startswith(".") or child.name == "__pycache__":
            continue
        if child.is_dir() and (child / "__init__.py").is_file():
            stems.add(child.name)
        elif child.suffix == ".py" and child.name != "__init__.py":
            stems.add(child.stem)
    return stems


def _verify_init_file(tree: ast.Module, init_dir: Path, rel_s: str) -> list[str]:
    from src.import_rules.verify_init_file_imports import verify_init_file_imports

    ok, msg = verify_init_file_imports(tree, init_dir)
    return [] if ok else [f"{rel_s}: {msg}"]


def verify_src_contract(src_root: Path | None = None) -> list[str]:
    from src.import_rules.verify_leaf_imports import verify_leaf_imports
    from src.import_rules.verify_shared_imports import verify_shared_imports
    from src.import_rules.verify_single_named_function import verify_single_named_function

    root = src_root or _repo_src()
    issues: list[str] = []
    issues.extend(_verify_top_level_exports(root))
    issues.extend(_verify_subpackage_exports(root))

    for path in sorted(root.rglob("*.py")):
        rel = path.relative_to(root)
        rel_s = rel.as_posix()
        if rel_s in _SKIP_FILES or any(rel_s.startswith(p) for p in _SKIP_PREFIXES):
            continue
        if rel.parts[0] == "import_rules":
            continue

        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            issues.append(f"{rel_s}: syntax error: {exc}")
            continue

        if path.name == "__init__.py":
            issues.extend(_verify_init_file(tree, path.parent, rel_s))
            pkg = path.parent.name
            ok, msg = verify_single_named_function(tree, pkg)
            if not ok:
                issues.append(f"{rel_s}: {msg}")
            continue

        if rel.parts[0] == "shared":
            if path.name == "__init__.py":
                issues.extend(_verify_init_file(tree, path.parent, rel_s))
                pkg = path.parent.name if len(rel.parts) > 2 else "shared"
                ok, msg = verify_single_named_function(tree, pkg)
                if not ok:
                    issues.append(f"{rel_s}: {msg}")
                continue

            ok, msg = verify_shared_imports(tree)
            if not ok:
                issues.append(f"{rel_s}: {msg}")
            ok, msg = verify_single_named_function(tree, path.stem)
            if not ok:
                issues.append(f"{rel_s}: {msg}")
            continue

        if rel_s == "pipeline/errors/exceptions.py":
            continue

        ok, msg = verify_single_named_function(tree, path.stem)
        if not ok:
            issues.append(f"{rel_s}: {msg}")

        from src.import_rules.compiler_adapter_stems import is_compiler_adapter_stem

        if is_compiler_adapter_stem(path.stem):
            from src.import_rules.verify_adapter_file_imports import (
                verify_adapter_file_imports,
            )

            ok, msg = verify_adapter_file_imports(tree, src_root=root)
            if not ok:
                issues.append(f"{rel_s}: {msg}")
        else:
            ok, msg = verify_leaf_imports(tree)
            if not ok:
                issues.append(f"{rel_s}: {msg}")

    return issues


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    root = Path(argv[0]) if argv else _repo_src()
    issues = verify_src_contract(root)
    if issues:
        for line in issues:
            print(line)
        print(f"\n{len(issues)} contract issue(s)")
        return 1
    print("verify_src_contract: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
