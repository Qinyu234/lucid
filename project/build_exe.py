"""
Build script to package the CSF application as an exe.
"""

import subprocess
import sys
from pathlib import Path


def build_exe():
    """Build the exe using PyInstaller."""
    print("Building CSF Application exe...")
    print("=" * 60)
    
    # Run PyInstaller with the spec file
    result = subprocess.run(
        [sys.executable, '-m', 'PyInstaller', 'build_exe.spec'],
        cwd=Path(__file__).parent
    )
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("Build successful!")
        print("Exe location: project/dist/CSF_App.exe")
    else:
        print("\n" + "=" * 60)
        print("Build failed!")
        print("Check the output above for errors.")
    
    return result.returncode


if __name__ == '__main__':
    sys.exit(build_exe())
