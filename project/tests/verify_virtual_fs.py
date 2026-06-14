"""
Auto-generated verifier stub for core/vfs/virtual_fs.py
"""

from pathlib import Path
import ast


def test_virtual_fs_syntax():
    source_file = Path(__file__).resolve().parents[1] / 'core/vfs/virtual_fs.py'
    source = source_file.read_text(encoding="utf-8")
    ast.parse(source)
