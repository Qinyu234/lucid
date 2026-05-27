"""Verify a generated job workplace against codegen-user-contract."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def _package_dirs_missing_init(src_root: Path) -> list[str]:
    issues: list[str] = []
    for d in sorted(src_root.rglob("*")):
        if not d.is_dir():
            continue
        if d.name in ("__pycache__",):
            continue
        if any(p.name == "__pycache__" for p in d.parents):
            continue
        has_py_child = any(
            c.suffix == ".py" or (c.is_dir() and (c / "__init__.py").is_file())
            for c in d.iterdir()
            if c.name != "__pycache__"
        )
        if not has_py_child:
            continue
        if not (d / "__init__.py").is_file():
            issues.append(f"missing package interface: {d / '__init__.py'}")
    return issues


def verify_workplace_contract(job_root: Path, job_id: str | None = None) -> list[str]:
    import ast

    from src.import_rules.verify_generated_code import verify_generated_code
    from src.import_rules.verify_init_file_imports import verify_init_file_imports
    from src.import_rules.verify_user_shared_stem import verify_user_shared_stem

    job_root = Path(job_root)
    issues: list[str] = []
    src_root = job_root / "src"
    if not src_root.is_dir():
        return [f"missing {src_root}"]

    shared_dir = src_root / "shared"
    if shared_dir.is_dir():
        from src.import_rules.user_shared_allowlist import is_allowed_user_shared_category

        for py in sorted(shared_dir.rglob("*.py")):
            if py.name == "__init__.py":
                continue
            rel = py.relative_to(shared_dir)
            if len(rel.parts) == 1:
                ok, msg = verify_user_shared_stem(py.stem)
                if not ok:
                    issues.append(msg)
            elif len(rel.parts) == 2:
                category, _ = rel.parts
                if not is_allowed_user_shared_category(category):
                    issues.append(f"shared category {category!r} not allowed")
                ok, msg = verify_user_shared_stem(py.stem)
                if not ok:
                    issues.append(msg)
            else:
                issues.append(f"shared module too deep: {py.relative_to(job_root)}")
                continue
            code = py.read_text(encoding="utf-8")
            vok, vmsg = verify_generated_code(code, py.stem, "shared")
            if not vok:
                issues.append(f"{py}: {vmsg}")

    if job_id:
        job_pkg = src_root / job_id
        if not (job_pkg / "__init__.py").is_file():
            issues.append(f"missing src/{job_id}/__init__.py")

    issues.extend(_package_dirs_missing_init(src_root))

    for py in sorted(src_root.rglob("*.py")):
        if py.name == "__init__.py":
            rel_parent = py.parent
            child_modules = set()
            for c in rel_parent.iterdir():
                if c.is_dir() and (c / "__init__.py").is_file():
                    child_modules.add(c.name)
                elif c.suffix == ".py" and c.name != "__init__.py":
                    child_modules.add(c.stem)
            code = py.read_text(encoding="utf-8")
            from src.import_rules.verify_init_file_imports import verify_init_file_imports

            vok, vmsg = verify_init_file_imports(ast.parse(code), rel_parent)
            if not vok:
                issues.append(f"{py.relative_to(job_root)}: {vmsg}")
                continue
            vok, vmsg = verify_generated_code(
                code, rel_parent.name if rel_parent != src_root else "src", "init", child_modules=child_modules
            )
            if not vok:
                issues.append(f"{py.relative_to(job_root)}: {vmsg}")
            continue

        if shared_dir in py.parents:
            continue

        code = py.read_text(encoding="utf-8")
        rel = py.relative_to(job_root)
        if py.name.startswith("test_") and py.suffix == ".py":
            from src.pipeline.code_tree.generate_test.verify_test import verify_test

            leaf_fn = py.stem[5:] if py.stem.startswith("test_") else py.stem
            vok, vmsg = verify_test(code, leaf_fn)
            if not vok:
                issues.append(f"{rel}: {vmsg}")
            continue

        vok, vmsg = verify_generated_code(code, py.stem, "leaf")
        if not vok:
            issues.append(f"{rel}: {vmsg}")

    latest = job_root / "tree" / "latest.json"
    if latest.is_file():
        import json

        payload = json.loads(latest.read_text(encoding="utf-8"))
        tree = payload.get("tree") or {}

        def walk(node: dict):
            cp = node.get("code_path") or ""
            if cp.count("/src/") > 1 or cp.count("\\src\\") > 1:
                issues.append(f"nested src path in code_path: {cp}")
            for ch in node.get("children") or []:
                walk(ch)

        walk(tree)

    return issues


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: python -m src.verify_workplace_contract <job_root> [job_id]")
        return 2
    job_root = Path(argv[0])
    job_id = argv[1] if len(argv) > 1 else None
    issues = verify_workplace_contract(job_root, job_id=job_id)
    if issues:
        for line in issues:
            print(line)
        print(f"\n{len(issues)} workplace issue(s)")
        return 1
    print("verify_workplace_contract: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
