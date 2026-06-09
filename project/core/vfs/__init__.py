"""
Virtual File System
Maps inheritance trees to virtual files for editing.
"""

from typing import Dict, Any, List
from core.vfs.virtual_fs import VirtualFileSystem
from core.vfs.inheritance_mapper import map_inheritance_to_vfs
from core.vfs.image_virtual import ImageVirtualFile


def create_virtual_filesystem(csf: Dict[str, Any]) -> VirtualFileSystem:
    """
    Create a virtual file system from a desugared CSF.
    
    Args:
        csf: Desugared CSF structure
        
    Returns:
        VirtualFileSystem instance with virtual files mapped from inheritance trees
    """
    vfs = VirtualFileSystem()
    
    # Map inheritance trees to virtual files
    map_inheritance_to_vfs(csf, vfs)
    
    return vfs


__all__ = ['create_virtual_filesystem', 'VirtualFileSystem', 'map_inheritance_to_vfs', 'ImageVirtualFile']
