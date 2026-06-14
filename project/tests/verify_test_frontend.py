"""
Auto-generated verifier stub for examples/test_frontend.py
"""

from pathlib import Path
import ast


def test_test_frontend_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'examples/test_frontend.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
