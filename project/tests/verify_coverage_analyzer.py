"""
Auto-generated verifier stub for core/testing/coverage_analyzer.py
"""

from pathlib import Path
import ast


def test_coverage_analyzer_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/testing/coverage_analyzer.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
