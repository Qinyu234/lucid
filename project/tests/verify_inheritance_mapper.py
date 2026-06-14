"""
Auto-generated verifier stub for core/vfs/inheritance_mapper.py
"""

from pathlib import Path
import ast


def test_inheritance_mapper_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/vfs/inheritance_mapper.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
