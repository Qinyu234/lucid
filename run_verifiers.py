"""
Run all verifier scripts in the todo/ directory or test files in a target folder
"""
import subprocess
import sys
from pathlib import Path
import glob
import argparse


def collect_source_files(source_root: Path = Path("project")):
    """Collect project source files that should be covered by verifier scripts."""
    exclude_dirs = {"tests", "build"}
    return sorted(
        p for p in source_root.rglob("*.py")
        if not any(part in exclude_dirs for part in p.parts)
        and p.name != "__init__.py"
    )


def expected_verifier_name(
    source_path: Path,
    source_root: Path = Path("project"),
    stem_counts=None,
    existing_verifiers=None,
) -> str:
    """Build the expected verifier filename for a source file."""
    relative = source_path.relative_to(source_root).with_suffix("")
    stem = relative.name
    slug = "_".join(relative.parts)

    if stem_counts is None:
        stem_counts = {}
    if existing_verifiers is None:
        existing_verifiers = set()

    candidate = f"verify_{stem}.py"
    if stem_counts.get(stem, 0) == 1 and candidate not in existing_verifiers:
        return candidate

    return f"verify_{slug}.py"


def find_missing_verifier_scripts(
    source_root: Path = Path("project"),
    tests_root: Path = Path("project/tests")
):
    """Return a list of source files that do not have matching verifier scripts."""
    source_files = collect_source_files(source_root)
    existing_verifiers = {p.name for p in tests_root.glob("verify_*.py")}
    stem_counts = {}
    for source_path in source_files:
        stem_counts[source_path.stem] = stem_counts.get(source_path.stem, 0) + 1

    missing = []
    for source_path in source_files:
        expected_name = expected_verifier_name(
            source_path,
            source_root,
            stem_counts=stem_counts,
            existing_verifiers=existing_verifiers,
        )
        if expected_name not in existing_verifiers:
            missing.append((source_path, tests_root / expected_name))

    return missing


def create_verifier_stub(source_path: Path, test_path: Path) -> None:
    """Create a minimal verifier stub for a missing source module."""
    test_path.parent.mkdir(parents=True, exist_ok=True)
    relative_source_path = source_path.relative_to(Path("project"))
    stub = f'''"""
Auto-generated verifier stub for {source_path}
"""

from pathlib import Path
import ast


def test_{source_path.stem}_syntax():
    source_file = Path(__file__).resolve().parents[1] / {relative_source_path!r}
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
'''
    test_path.write_text(stub, encoding="utf-8")


def ensure_verifiers(source_root: Path = Path("project"), tests_root: Path = Path("project/tests"), dry_run: bool = False):
    missing = find_missing_verifier_scripts(source_root, tests_root)

    if not missing:
        print("All source modules have verifier scripts.")
        return 0

    print(f"Found {len(missing)} missing verifier scripts:")
    for source_path, test_path in missing:
        print(f"  {test_path.name} -> {source_path}")
        if not dry_run:
            create_verifier_stub(source_path, test_path)

    if dry_run:
        print("Dry run complete. No files were created.")
    else:
        print("Created missing verifier scripts.")

    return len(missing)


def run_todo_verifiers():
    """Run all verifier scripts in the project/tests/ directory."""
    verify_scripts = sorted(glob.glob("project/tests/verify_*.py"))
    
    print(f"Found {len(verify_scripts)} verifier scripts in project/tests/")
    print("=" * 60)
    
    results = {
        'passed': [],
        'failed': []
    }
    
    for script in verify_scripts:
        script_name = Path(script).name
        
        try:
            result = subprocess.run(
                [".venv/Scripts/python.exe", "-m", "pytest", script, "-v"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                results['passed'].append(script_name)
            else:
                results['failed'].append(script_name)
        except subprocess.TimeoutExpired:
            results['failed'].append(script_name)
        except Exception as e:
            results['failed'].append(script_name)
    
    return results

def run_folder_tests(target_folder):
    """Run pytest on all Python files in the target folder."""
    target_path = Path(target_folder)
    
    if not target_path.exists():
        print(f"Error: Folder {target_folder} does not exist")
        sys.exit(1)
    
    # Find all Python files in the folder
    py_files = sorted(target_path.rglob("*.py"))
    
    if not py_files:
        print(f"No Python files found in {target_folder}")
        sys.exit(0)
    
    print(f"Found {len(py_files)} Python files in {target_folder}")
    print("=" * 60)
    
    results = {
        'passed': [],
        'failed': []
    }
    
    for py_file in py_files:
        file_name = py_file.relative_to(target_path)
        
        try:
            result = subprocess.run(
                [".venv/Scripts/python.exe", "-m", "pytest", str(py_file), "-v"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                results['passed'].append(str(file_name))
            else:
                results['failed'].append(str(file_name))
        except subprocess.TimeoutExpired:
            results['failed'].append(str(file_name))
        except Exception as e:
            results['failed'].append(str(file_name))
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run verifiers or test files")
    parser.add_argument("--folder", help="Target folder to test all Python files")
    parser.add_argument(
        "--ensure-verifiers",
        action="store_true",
        help="Generate missing verifier scripts for source files."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show missing verifier scripts without creating files."
    )
    args = parser.parse_args()

    if args.ensure_verifiers:
        missing_count = ensure_verifiers(dry_run=args.dry_run)
        if args.dry_run and missing_count:
            sys.exit(1)
        sys.exit(0)

    if args.folder:
        results = run_folder_tests(args.folder)
    else:
        results = run_todo_verifiers()

    print("\n" + "=" * 60)
    print(f"Summary: {len(results['passed'])} passed, {len(results['failed'])} failed")

    if results['passed']:
        print("\nPassed:")
        for item in results['passed']:
            print(f"  ✓ {item}")

    if results['failed']:
        print("\nFailed:")
        for item in results['failed']:
            print(f"  ✗ {item}")
        sys.exit(1)
    else:
        sys.exit(0)
