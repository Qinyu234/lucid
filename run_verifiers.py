"""
Run all verifier scripts in the todo/ directory or test files in a target folder
"""
import subprocess
import sys
from pathlib import Path
import glob
import argparse

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
    args = parser.parse_args()
    
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
