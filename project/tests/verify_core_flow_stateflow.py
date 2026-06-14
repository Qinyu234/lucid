"""
Auto-generated verifier stub for core/flow/stateflow.py
"""

from pathlib import Path
import ast


def test_stateflow_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/flow/stateflow.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
