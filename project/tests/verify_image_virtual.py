"""
Auto-generated verifier stub for core/vfs/image_virtual.py
"""

from pathlib import Path
import ast


def test_image_virtual_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/vfs/image_virtual.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
