"""
Auto-generated verifier stub for examples/test_solar.py
"""

from pathlib import Path
import ast


def test_test_solar_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'examples/test_solar.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
