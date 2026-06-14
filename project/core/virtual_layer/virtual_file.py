"""
Virtual File System for Lucid
A projection layer over real code for safe editing
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class VirtualFile:
    """
    Represents a virtual file in the projection layer.
    Edits here are tracked and can be diffed/patched back to real files.
    """
    path: str
    original_content: str
    modified_content: str = ""
    is_modified: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.modified_content:
            self.modified_content = self.original_content
    
    def apply_edit(self, new_content: str) -> None:
        """Apply an edit to the virtual file."""
        self.modified_content = new_content
        self.is_modified = True
    
    def get_diff(self) -> str:
        """Get the diff between original and modified content."""
        if not self.is_modified:
            return ""
        
        original_lines = self.original_content.split('\n')
        modified_lines = self.modified_content.split('\n')
        
        # Simple line-by-line diff
        diff_lines = []
        for i, (orig, mod) in enumerate(zip(original_lines, modified_lines)):
            if orig != mod:
                diff_lines.append(f"- {orig}")
                diff_lines.append(f"+ {mod}")
        
        # Handle length differences
        if len(original_lines) > len(modified_lines):
            for line in original_lines[len(modified_lines):]:
                diff_lines.append(f"- {line}")
        elif len(modified_lines) > len(original_lines):
            for line in modified_lines[len(original_lines):]:
                diff_lines.append(f"+ {line}")
        
        return '\n'.join(diff_lines)
    
    def reset(self) -> None:
        """Reset to original content."""
        self.modified_content = self.original_content
        self.is_modified = False


class VirtualFileSystem:
    """
    Manages a collection of virtual files.
    Provides diff/patch capabilities for editing real code safely.
    """
    
    def __init__(self):
        self.files: Dict[str, VirtualFile] = {}
    
    def add_file(self, path: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> VirtualFile:
        """
        Add a virtual file.
        
        Args:
            path: Virtual file path
            content: File content
            metadata: Optional metadata
            
        Returns:
            VirtualFile instance
        """
        vfile = VirtualFile(
            path=path,
            original_content=content,
            metadata=metadata or {}
        )
        self.files[path] = vfile
        return vfile
    
    def get_file(self, path: str) -> Optional[VirtualFile]:
        """Get a virtual file by path."""
        return self.files.get(path)
    
    def get_all_files(self) -> List[str]:
        """Get all virtual file paths."""
        return list(self.files.keys())
    
    def get_modified_files(self) -> List[str]:
        """Get paths of all modified files."""
        return [path for path, vfile in self.files.items() if vfile.is_modified]
    
    def compute_all_diffs(self) -> Dict[str, str]:
        """Compute diffs for all modified files."""
        diffs = {}
        for path, vfile in self.files.items():
            if vfile.is_modified:
                diffs[path] = vfile.get_diff()
        return diffs
    
    def reset_all(self) -> None:
        """Reset all virtual files to original content."""
        for vfile in self.files.values():
            vfile.reset()
    
    def regenerate_from_source(self, source_path: str, parsed_data: Dict[str, Any]) -> None:
        """
        Regenerate virtual files from source when real files change externally.
        
        Args:
            source_path: Path to the source file
            parsed_data: Parsed code data
        """
        # Clear all virtual files when regenerating from source
        # This ensures a clean slate for the new projection
        self.files.clear()
        
        # Create new virtual files based on parsed structure
        # For now, create one virtual file per function/class
        for func in parsed_data.get('functions', []):
            func_path = f"{source_path}:func:{func['name']}"
            self.add_file(func_path, f"# Function: {func['name']}\n# Line: {func['line']}\n")
        
        for cls in parsed_data.get('classes', []):
            class_path = f"{source_path}:class:{cls['name']}"
            self.add_file(class_path, f"# Class: {cls['name']}\n# Line: {cls['line']}\n")
