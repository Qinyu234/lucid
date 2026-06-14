"""
Auto-generated verifier stub for core/complexity/complexity_estimator.py
"""

from pathlib import Path
import ast


def test_complexity_estimator_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/complexity/complexity_estimator.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
