"""
Auto-generated verifier stub for core/expansion/nesting_guard.py
"""

from pathlib import Path
import ast


def test_nesting_guard_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/expansion/nesting_guard.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
