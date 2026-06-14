"""
Auto-generated verifier stub for core/desugar/state_explicit.py
"""

from pathlib import Path
import ast


def test_state_explicit_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/desugar/state_explicit.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
