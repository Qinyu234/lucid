"""
Auto-generated verifier stub for core/expansion/dependency_graph.py
"""

from pathlib import Path
import ast


def test_dependency_graph_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/expansion/dependency_graph.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
