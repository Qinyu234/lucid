"""
Auto-generated verifier stub for core/desugar/class_to_func.py
"""

from pathlib import Path
import ast


def test_class_to_func_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/desugar/class_to_func.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
