"""
Auto-generated verifier stub for build_exe.py
"""

from pathlib import Path
import ast


def test_build_exe_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'build_exe.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
