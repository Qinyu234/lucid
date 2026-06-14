"""
Auto-generated verifier stub for examples/inherit_sample.py
"""

from pathlib import Path
import ast


def test_inherit_sample_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'examples/inherit_sample.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
