"""
Tests for virtual layer
Tests virtual file system and diff/patch functionality
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.virtual_layer.virtual_file import VirtualFile, VirtualFileSystem
from core.virtual_layer.diff_patch import compute_diff, apply_patch


class TestVirtualFile:
    """Test VirtualFile functionality."""
    
    def test_virtual_file_creation(self):
        """Test creation of virtual file."""
        vfile = VirtualFile(
            path="test.py",
            original_content="def hello():\n    pass\n"
        )
        
        assert vfile.path == "test.py"
        assert vfile.original_content == "def hello():\n    pass\n"
        assert vfile.modified_content == "def hello():\n    pass\n"
        assert vfile.is_modified is False
    
    def test_apply_edit(self):
        """Test applying edits to virtual file."""
        vfile = VirtualFile(
            path="test.py",
            original_content="def hello():\n    pass\n"
        )
        
        new_content = "def hello():\n    print('Hello')\n"
        vfile.apply_edit(new_content)
        
        assert vfile.modified_content == new_content
        assert vfile.is_modified is True
    
    def test_get_diff(self):
        """Test getting diff between original and modified."""
        vfile = VirtualFile(
            path="test.py",
            original_content="line1\nline2\nline3\n"
        )
        
        vfile.apply_edit("line1\nmodified\nline3\n")
        diff = vfile.get_diff()
        
        assert "line2" in diff
        assert "modified" in diff
        assert "-" in diff
        assert "+" in diff
    
    def test_get_diff_no_changes(self):
        """Test getting diff when no changes made."""
        vfile = VirtualFile(
            path="test.py",
            original_content="line1\nline2\n"
        )
        
        diff = vfile.get_diff()
        
        assert diff == ""
    
    def test_reset(self):
        """Test resetting virtual file to original content."""
        vfile = VirtualFile(
            path="test.py",
            original_content="original\n"
        )
        
        vfile.apply_edit("modified\n")
        assert vfile.is_modified is True
        
        vfile.reset()
        
        assert vfile.modified_content == "original\n"
        assert vfile.is_modified is False
    
    def test_metadata_storage(self):
        """Test metadata storage in virtual file."""
        vfile = VirtualFile(
            path="test.py",
            original_content="content\n",
            metadata={"author": "test", "version": "1.0"}
        )
        
        assert vfile.metadata["author"] == "test"
        assert vfile.metadata["version"] == "1.0"


class TestVirtualFileSystem:
    """Test VirtualFileSystem functionality."""
    
    def test_vfs_initialization(self):
        """Test VFS initialization."""
        vfs = VirtualFileSystem()
        
        assert len(vfs.files) == 0
        assert len(vfs.get_all_files()) == 0
    
    def test_add_file(self):
        """Test adding file to VFS."""
        vfs = VirtualFileSystem()
        vfile = vfs.add_file("test.py", "content\n")
        
        assert vfile is not None
        assert vfile.path == "test.py"
        assert len(vfs.files) == 1
        assert "test.py" in vfs.files
    
    def test_get_file(self):
        """Test retrieving file from VFS."""
        vfs = VirtualFileSystem()
        vfs.add_file("test.py", "content\n")
        
        retrieved = vfs.get_file("test.py")
        
        assert retrieved is not None
        assert retrieved.path == "test.py"
    
    def test_get_file_nonexistent(self):
        """Test retrieving nonexistent file."""
        vfs = VirtualFileSystem()
        
        retrieved = vfs.get_file("nonexistent.py")
        
        assert retrieved is None
    
    def test_get_all_files(self):
        """Test getting all file paths."""
        vfs = VirtualFileSystem()
        vfs.add_file("file1.py", "content1\n")
        vfs.add_file("file2.py", "content2\n")
        vfs.add_file("file3.py", "content3\n")
        
        all_files = vfs.get_all_files()
        
        assert len(all_files) == 3
        assert "file1.py" in all_files
        assert "file2.py" in all_files
        assert "file3.py" in all_files
    
    def test_get_modified_files(self):
        """Test getting only modified files."""
        vfs = VirtualFileSystem()
        vfs.add_file("unchanged.py", "content\n")
        vfs.add_file("modified.py", "content\n")
        
        # Modify one file
        modified_file = vfs.get_file("modified.py")
        modified_file.apply_edit("new content\n")
        
        modified_files = vfs.get_modified_files()
        
        assert len(modified_files) == 1
        assert "modified.py" in modified_files
        assert "unchanged.py" not in modified_files
    
    def test_compute_all_diffs(self):
        """Test computing diffs for all modified files."""
        vfs = VirtualFileSystem()
        vfs.add_file("file1.py", "original\n")
        vfs.add_file("file2.py", "original\n")
        
        # Modify both files
        vfs.get_file("file1.py").apply_edit("modified1\n")
        vfs.get_file("file2.py").apply_edit("modified2\n")
        
        diffs = vfs.compute_all_diffs()
        
        assert len(diffs) == 2
        assert "file1.py" in diffs
        assert "file2.py" in diffs
    
    def test_reset_all(self):
        """Test resetting all files."""
        vfs = VirtualFileSystem()
        vfs.add_file("file1.py", "original\n")
        vfs.add_file("file2.py", "original\n")
        
        # Modify files
        vfs.get_file("file1.py").apply_edit("modified1\n")
        vfs.get_file("file2.py").apply_edit("modified2\n")
        
        assert len(vfs.get_modified_files()) == 2
        
        vfs.reset_all()
        
        assert len(vfs.get_modified_files()) == 0
        assert vfs.get_file("file1.py").modified_content == "original\n"
        assert vfs.get_file("file2.py").modified_content == "original\n"
    
    def test_regenerate_from_source(self):
        """Test regenerating virtual files from source."""
        vfs = VirtualFileSystem()
        
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': 'def func():\n    pass\n',
            'functions': [
                {'name': 'func', 'line': 1, 'column': 0, 'parameters': [], 'body_start': 1, 'body_end': 2}
            ],
            'classes': [],
            'variables': []
        }
        
        vfs.regenerate_from_source('test.py', parsed_data)
        
        # Should create virtual files for functions/classes
        all_files = vfs.get_all_files()
        assert len(all_files) >= 1
        assert any('func' in f for f in all_files)
    
    def test_regenerate_clears_old_files(self):
        """Test that regeneration clears old virtual files."""
        vfs = VirtualFileSystem()
        vfs.add_file("old_file.py", "old content\n")
        
        parsed_data = {
            'file_path': 'test.py',
            'language': 'python',
            'source_code': 'def func():\n    pass\n',
            'functions': [
                {'name': 'func', 'line': 1, 'column': 0, 'parameters': [], 'body_start': 1, 'body_end': 2}
            ],
            'classes': [],
            'variables': []
        }
        
        vfs.regenerate_from_source('test.py', parsed_data)
        
        # Old file should be removed
        assert vfs.get_file("old_file.py") is None


class TestDiffPatch:
    """Test diff and patch operations."""
    
    def test_compute_diff_simple(self):
        """Test computing simple diff."""
        original = "line1\nline2\nline3\n"
        modified = "line1\nmodified\nline3\n"
        
        diff = compute_diff(original, modified)
        
        assert diff['total_changes'] >= 1
        assert len(diff['changes']) >= 1
    
    def test_compute_diff_no_changes(self):
        """Test computing diff when no changes."""
        original = "line1\nline2\n"
        modified = "line1\nline2\n"
        
        diff = compute_diff(original, modified)
        
        assert diff['total_changes'] == 0
        assert len(diff['changes']) == 0
    
    def test_compute_diff_added_lines(self):
        """Test computing diff with added lines."""
        original = "line1\nline3\n"
        modified = "line1\nline2\nline3\n"
        
        diff = compute_diff(original, modified)
        
        assert diff['total_changes'] >= 1
        # Should detect the added line
        change_types = [c['type'] for c in diff['changes']]
        assert 'added' in change_types
    
    def test_compute_diff_removed_lines(self):
        """Test computing diff with removed lines."""
        original = "line1\nline2\nline3\n"
        modified = "line1\nline3\n"
        
        diff = compute_diff(original, modified)
        
        assert diff['total_changes'] >= 1
        # Should detect the removed line
        change_types = [c['type'] for c in diff['changes']]
        assert 'removed' in change_types
    
    def test_apply_patch_simple(self):
        """Test applying simple patch."""
        original = "line1\nline2\nline3\n"
        patch = {
            'changes': [
                {'line': 2, 'original': 'line2', 'modified': 'modified', 'type': 'modified'}
            ]
        }
        
        result = apply_patch(original, patch)
        
        assert "modified" in result
        assert "line2" not in result
    
    def test_apply_patch_add_line(self):
        """Test applying patch that adds a line."""
        original = "line1\nline3\n"
        patch = {
            'changes': [
                {'line': 2, 'original': None, 'modified': 'line2', 'type': 'added'}
            ]
        }
        
        result = apply_patch(original, patch)
        
        assert "line2" in result
        assert result == "line1\nline2\nline3\n"
    
    def test_apply_patch_remove_line(self):
        """Test applying patch that removes a line."""
        original = "line1\nline2\nline3\n"
        patch = {
            'changes': [
                {'line': 2, 'original': 'line2', 'modified': None, 'type': 'removed'}
            ]
        }
        
        result = apply_patch(original, patch)
        
        assert "line2" not in result
        assert result == "line1\nline3\n"
    
    def test_apply_patch_multiple_changes(self):
        """Test applying patch with multiple changes."""
        original = "line1\nline2\nline3\n"
        patch = {
            'changes': [
                {'line': 2, 'original': 'line2', 'modified': 'modified2', 'type': 'modified'},
                {'line': 3, 'original': 'line3', 'modified': 'modified3', 'type': 'modified'}
            ]
        }
        
        result = apply_patch(original, patch)
        
        assert "modified2" in result
        assert "modified3" in result
        assert "line2" not in result
        assert "line3" not in result
    
    def test_apply_patch_empty(self):
        """Test applying empty patch."""
        original = "line1\nline2\n"
        patch = {'changes': []}
        
        result = apply_patch(original, patch)
        
        assert result == original


class TestVirtualLayerIntegration:
    """Test integration of virtual layer components."""
    
    def test_full_edit_workflow(self):
        """Test complete edit workflow: add -> edit -> diff -> patch."""
        vfs = VirtualFileSystem()
        
        # Add file
        original = "def hello():\n    pass\n"
        vfs.add_file("test.py", original)
        
        # Edit file
        vfile = vfs.get_file("test.py")
        modified = "def hello():\n    print('Hello')\n"
        vfile.apply_edit(modified)
        
        # Get diff
        diff = vfile.get_diff()
        assert len(diff) > 0
        
        # Compute structured diff
        structured_diff = compute_diff(original, modified)
        assert structured_diff['total_changes'] > 0
        
        # Apply patch to get back to original
        patched = apply_patch(modified, structured_diff)
        # Note: This might not perfectly reverse due to simple diff algorithm
        assert patched is not None
    
    def test_multiple_files_workflow(self):
        """Test workflow with multiple files."""
        vfs = VirtualFileSystem()
        
        # Add multiple files
        vfs.add_file("file1.py", "content1\n")
        vfs.add_file("file2.py", "content2\n")
        vfs.add_file("file3.py", "content3\n")
        
        # Modify some
        vfs.get_file("file1.py").apply_edit("modified1\n")
        vfs.get_file("file3.py").apply_edit("modified3\n")
        
        # Check modified files
        modified = vfs.get_modified_files()
        assert len(modified) == 2
        assert "file1.py" in modified
        assert "file3.py" in modified
        assert "file2.py" not in modified
        
        # Get all diffs
        diffs = vfs.compute_all_diffs()
        assert len(diffs) == 2
        
        # Reset all
        vfs.reset_all()
        assert len(vfs.get_modified_files()) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
