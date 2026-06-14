"""
Auto-generated verifier stub for core/expansion/mutation.py
"""

from pathlib import Path
import ast


def test_mutation_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/expansion/mutation.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
