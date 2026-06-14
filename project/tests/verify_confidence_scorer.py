"""
Auto-generated verifier stub for core/complexity/confidence_scorer.py
"""

from pathlib import Path
import ast


def test_confidence_scorer_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/complexity/confidence_scorer.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
