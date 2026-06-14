"""
Auto-generated verifier stub for core/flow/state_visualizer.py
"""

from pathlib import Path
import ast


def test_state_visualizer_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/flow/state_visualizer.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
