"""
Virtual Layer - Code projection and editing
Provides a virtual file system for editing without touching original files
"""

from .virtual_file import VirtualFile, VirtualFileSystem
from .diff_patch import compute_diff, apply_patch

__all__ = ['VirtualFile', 'VirtualFileSystem', 'compute_diff', 'apply_patch']
