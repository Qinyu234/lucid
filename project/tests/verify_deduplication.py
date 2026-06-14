"""
Auto-generated verifier stub for core/expansion/deduplication.py
"""

from pathlib import Path
import ast


def test_deduplication_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/expansion/deduplication.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
