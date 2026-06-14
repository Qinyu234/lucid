"""
Auto-generated verifier stub for core/sync/writer/extract.py
"""

from pathlib import Path
import ast


def test_extract_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/sync/writer/extract.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
