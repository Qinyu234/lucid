"""
Auto-generated verifier stub for core/csf/schema.py
"""

from pathlib import Path
import ast


def test_schema_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/csf/schema.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
