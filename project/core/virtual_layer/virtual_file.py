"""
Virtual File System for Lucid
Based on ARCHITECTURE.html specification
A projection layer over real code for safe editing
Pattern: VSCode FileSystemProvider API, TextDocumentContentProvider, diff engine, file watcher
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from pathlib import Path
import time


@dataclass
class VirtualFile:
    """
    Represents a virtual file in the projection layer per ARCHITECTURE.html.
    Edits here are tracked and can be diffed/patched back to real files.
    Pattern: VSCode TextDocumentContentProvider
    """
    path: str
    original_content: str
    modified_content: str = ""
    is_modified: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    last_modified: float = field(default_factory=time.time)
    
    def __post_init__(self):
        if not self.modified_content:
            self.modified_content = self.original_content
    
    def apply_edit(self, new_content: str) -> None:
        """Apply an edit to the virtual file."""
        self.modified_content = new_content
        self.is_modified = True
        self.last_modified = time.time()
    
    def get_diff(self) -> str:
        """
        Get the diff between original and modified content.
        Pattern: VSCode built-in diff engine
        """
        if not self.is_modified:
            return ""
        
        original_lines = self.original_content.split('\n')
        modified_lines = self.modified_content.split('\n')
        
        # Simple line-by-line diff (conceptually matches VSCode diff engine)
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
        self.last_modified = time.time()


class VirtualFileSystem:
    """
    Manages a collection of virtual files per ARCHITECTURE.html.
    Pattern: VSCode FileSystemProvider API
    Provides diff/patch capabilities for editing real code safely.
    Uses file watching pattern (chokidar equivalent) for external changes.
    """
    
    def __init__(self):
        self.files: Dict[str, VirtualFile] = {}
        self.pending_diffs: Dict[str, str] = {}  # Pending diffs to apply after regeneration
        self.file_watchers: Dict[str, float] = {}  # File modification timestamps (chokidar pattern)
    
    def add_file(self, path: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> VirtualFile:
        """
        Add a virtual file.
        Pattern: VSCode FileSystemProvider API
        
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
        """
        Compute diffs for all modified files.
        Pattern: VSCode diff engine
        """
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
        Per ARCHITECTURE.html: real layer external changes trigger full re-parse and virtual layer regeneration.
        Pattern: chokidar file watcher → full re-parse → virtual layer regeneration → pending diff overlay
        
        Args:
            source_path: Path to the source file
            parsed_data: Parsed code data
        """
        # Save pending diffs before regeneration
        pending_diffs = self.compute_all_diffs()
        
        # Clear all virtual files when regenerating from source
        # This ensures a clean slate for the new projection
        self.files.clear()
        
        # Create new virtual files based on parsed structure
        # Per ARCHITECTURE: reorganize code by access contracts
        # For now, create one virtual file per function/class as a projection
        for func in parsed_data.get('functions', []):
            func_path = f"{source_path}:func:{func['name']}"
            self.add_file(func_path, f"# Function: {func['name']}\n# Line: {func['line']}\n")
        
        for cls in parsed_data.get('classes', []):
            class_path = f"{source_path}:class:{cls['name']}"
            self.add_file(class_path, f"# Class: {cls['name']}\n# Line: {cls['line']}\n")
        
        # Try to overlay pending diffs (Nix atomic model per ARCHITECTURE)
        # In a real implementation, this would use 3-way merge
        self.pending_diffs = pending_diffs
    
    def watch_file(self, file_path: str) -> None:
        """
        Watch a file for external changes.
        Pattern: chokidar file watcher
        
        Args:
            file_path: Path to watch
        """
        self.file_watchers[file_path] = time.time()
    
    def check_external_changes(self, file_path: str, current_mtime: float) -> bool:
        """
        Check if a file has been modified externally.
        Pattern: chokidar file watcher
        
        Args:
            file_path: Path to check
            current_mtime: Current modification time
            
        Returns:
            True if file was modified externally
        """
        if file_path in self.file_watchers:
            return current_mtime > self.file_watchers[file_path]
        return False
    
    def apply_patch(self, file_path: str, patch: Dict[str, Any]) -> bool:
        """
        Apply a patch to a real file.
        Per ARCHITECTURE: changes compute diff → patch back to real layer
        Pattern: Nix atomic model - patch input is fully determined, result doesn't depend on operation order
        
        Args:
            file_path: Path to the real file
            patch: Patch dictionary with changes
            
        Returns:
            True if patch was applied successfully
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply patch using diff_patch utilities
            from .diff_patch import apply_patch
            patched_content = apply_patch(content, patch)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(patched_content)
            
            # Update watcher timestamp
            self.file_watchers[file_path] = time.time()
            
            return True
        except Exception as e:
            print(f"Error applying patch: {e}")
            return False
    
    def delete_file(self, path: str) -> bool:
        """
        Delete a virtual file.
        Pattern: VSCode FileSystemProvider API
        
        Args:
            path: Path to delete
            
        Returns:
            True if file was deleted, False if not found
        """
        if path in self.files:
            del self.files[path]
            return True
        return False
    
    def list_directory(self, path: str = "") -> List[str]:
        """
        List virtual files in a directory.
        Pattern: VSCode FileSystemProvider API
        
        Args:
            path: Directory path (empty string for root)
            
        Returns:
            List of file paths in the directory
        """
        if not path:
            return list(self.files.keys())
        
        # Filter files that start with the given path
        return [f for f in self.files.keys() if f.startswith(path)]
    
    def get_projection_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the virtual layer projection.
        Per ARCHITECTURE: virtual layer shows reorganized structure by writers/readers
        """
        return {
            'total_files': len(self.files),
            'modified_files': len(self.get_modified_files()),
            'pending_diffs': len(self.pending_diffs),
            'watched_files': len(self.file_watchers),
        }
