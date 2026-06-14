"""
Auto-generated verifier stub for core/flow/dataflow.py
"""

from pathlib import Path
import ast


def test_dataflow_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/flow/dataflow.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
