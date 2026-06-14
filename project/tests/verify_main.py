"""
Auto-generated verifier stub for app/main.py
"""

from pathlib import Path
import ast


def test_main_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'app/main.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
