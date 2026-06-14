"""
Auto-generated verifier stub for cli/tree_printer.py
"""

from pathlib import Path
import ast


def test_tree_printer_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'cli/tree_printer.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
