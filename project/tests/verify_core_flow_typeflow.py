"""
Auto-generated verifier stub for core/flow/typeflow.py
"""

from pathlib import Path
import ast


def test_typeflow_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/flow/typeflow.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
