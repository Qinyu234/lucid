"""
Auto-generated verifier stub for core/testing/test_generator.py
"""

from pathlib import Path
import ast


def test_test_generator_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/testing/test_generator.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
