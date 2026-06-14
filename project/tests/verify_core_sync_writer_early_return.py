"""
Auto-generated verifier stub for core/sync/writer/early_return.py
"""

from pathlib import Path
import ast


def test_early_return_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/sync/writer/early_return.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
