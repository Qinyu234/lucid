"""
Run all verifier scripts in the todo/ directory
"""
import subprocess
import sys
from pathlib import Path
import glob

# Find all verify scripts
verify_scripts = sorted(glob.glob("todo/verify_task_*.py"))

print(f"Found {len(verify_scripts)} verifier scripts")
print("=" * 60)

results = {
    'passed': [],
    'failed': []
}

for script in verify_scripts:
    script_name = Path(script).name
    print(f"\nRunning {script_name}...")
    
    try:
        result = subprocess.run(
            [".venv/Scripts/python.exe", script],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✓ {script_name} PASSED")
            results['passed'].append(script_name)
        else:
            print(f"✗ {script_name} FAILED")
            print(f"  Error: {result.stderr}")
            results['failed'].append(script_name)
    except subprocess.TimeoutExpired:
        print(f"✗ {script_name} TIMEOUT")
        results['failed'].append(script_name)
    except Exception as e:
        print(f"✗ {script_name} ERROR: {e}")
        results['failed'].append(script_name)

print("\n" + "=" * 60)
print(f"Summary: {len(results['passed'])} passed, {len(results['failed'])} failed")

if results['failed']:
    print("\nFailed scripts:")
    for script in results['failed']:
        print(f"  - {script}")
    sys.exit(1)
else:
    print("\nAll verifiers passed!")
    sys.exit(0)
