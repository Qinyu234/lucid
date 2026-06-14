"""
Auto-generated verifier stub for examples/mutation_sample.py
"""

from pathlib import Path
import ast


def test_mutation_sample_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'examples/mutation_sample.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
