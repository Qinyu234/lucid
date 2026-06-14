"""
Auto-generated verifier stub for core/desugar/inheritance_decompose.py
"""

from pathlib import Path
import ast


def test_inheritance_decompose_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/desugar/inheritance_decompose.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
