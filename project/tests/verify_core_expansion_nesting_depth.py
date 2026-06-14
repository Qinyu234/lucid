"""
Auto-generated verifier stub for core/expansion/nesting_depth.py
"""

from pathlib import Path
import ast


def test_nesting_depth_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/expansion/nesting_depth.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
