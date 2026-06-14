"""
Auto-generated verifier stub for core/sync/parser.py
"""

from pathlib import Path
import ast


def test_parser_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/sync/parser.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
