"""
Auto-generated verifier stub for core/testing/test_runner.py
"""

from pathlib import Path
import ast


def test_test_runner_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/testing/test_runner.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
