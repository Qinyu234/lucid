"""
Virtual File System
Manages virtual files that represent desugared code structures.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class VirtualFile:
    """Represents a virtual file in the virtual file system."""
    
    def __init__(self, path: str, content: str = "", file_type: str = "code"):
        """
        Initialize a virtual file.
        
        Args:
            path: Virtual file path
            content: File content
            file_type: Type of file (code, image, etc.)
        """
        self.path = path
        self.content = content
        self.file_type = file_type
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        self.metadata = {}
    
    def update_content(self, new_content: str) -> None:
        """Update file content and modification time."""
        self.content = new_content
        self.modified_at = datetime.now()
    
    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata key-value pair."""
        self.metadata[key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value."""
        return self.metadata.get(key, default)


class VirtualFileSystem:
    """Manages a collection of virtual files."""
    
    def __init__(self):
        """Initialize an empty virtual file system."""
        self.files: Dict[str, VirtualFile] = {}
        self.root_path = "/virtual"
    
    def create_file(self, path: str, content: str = "", file_type: str = "code") -> VirtualFile:
        """
        Create a new virtual file.
        
        Args:
            path: Virtual file path
            content: File content
            file_type: Type of file
            
        Returns:
            Created VirtualFile instance
        """
        full_path = f"{self.root_path}/{path.lstrip('/')}"
        virtual_file = VirtualFile(full_path, content, file_type)
        self.files[full_path] = virtual_file
        return virtual_file
    
    def get_file(self, path: str) -> Optional[VirtualFile]:
        """
        Get a virtual file by path.
        
        Args:
            path: Virtual file path
            
        Returns:
            VirtualFile instance if exists, None otherwise
        """
        full_path = f"{self.root_path}/{path.lstrip('/')}"
        return self.files.get(full_path)
    
    def update_file(self, path: str, new_content: str) -> bool:
        """
        Update a virtual file's content.
        
        Args:
            path: Virtual file path
            new_content: New content
            
        Returns:
            True if file exists and was updated, False otherwise
        """
        virtual_file = self.get_file(path)
        if virtual_file:
            virtual_file.update_content(new_content)
            return True
        return False
    
    def delete_file(self, path: str) -> bool:
        """
        Delete a virtual file.
        
        Args:
            path: Virtual file path
            
        Returns:
            True if file existed and was deleted, False otherwise
        """
        full_path = f"{self.root_path}/{path.lstrip('/')}"
        if full_path in self.files:
            del self.files[full_path]
            return True
        return False
    
    def list_files(self, directory: str = "") -> List[str]:
        """
        List all files in a directory.
        
        Args:
            directory: Directory path (empty for root)
            
        Returns:
            List of file paths
        """
        prefix = f"{self.root_path}/{directory.lstrip('/')}"
        if not prefix.endswith('/'):
            prefix += '/'
        
        return [path for path in self.files.keys() if path.startswith(prefix)]
    
    def get_all_files(self) -> Dict[str, VirtualFile]:
        """Get all virtual files."""
        return self.files.copy()


__all__ = ['VirtualFile', 'VirtualFileSystem']
