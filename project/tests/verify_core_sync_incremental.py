"""
Auto-generated verifier stub for core/sync/incremental.py
"""

from pathlib import Path
import ast


def test_incremental_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/sync/incremental.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
