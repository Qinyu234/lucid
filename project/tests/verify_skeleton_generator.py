"""
Auto-generated verifier stub for core/flow/skeleton_generator.py
"""

from pathlib import Path
import ast


def test_skeleton_generator_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/flow/skeleton_generator.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
