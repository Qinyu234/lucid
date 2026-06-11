"""
Test for virtual file editing functionality
验证虚拟文件编辑功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.vfs import create_virtual_filesystem
from core.expansion import expand
from core.desugar import desugar


def test_virtual_file_edit():
    """
    Test that virtual files can be edited through the interface.
    测试能够通过界面编辑虚拟文件。
    """
    test_code = """
class MyClass:
    def method1(self):
        return 1
    
    def method2(self):
        return 2
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        vfs = create_virtual_filesystem(csf)
        
        # Get a virtual file
        files = vfs.get_all_files()
        assert len(files) > 0, "Should have virtual files"
        
        # Get the first file and extract relative path
        file_path, virtual_file = list(files.items())[0]
        # Remove the root prefix to get relative path
        relative_path = file_path.replace(vfs.root_path + '/', '')
        
        # Edit the file
        new_content = "# Edited content\ndef new_function():\n    pass"
        success = vfs.update_file(relative_path, new_content)
        
        assert success, "Should successfully update virtual file"
        
        # Verify the change
        updated_file = vfs.get_file(relative_path)
        assert updated_file.content == new_content, "Content should be updated"
    finally:
        Path(temp_path).unlink()


def test_virtual_file_edit_persistence():
    """
    Test that virtual file edits are persisted.
    测试虚拟文件编辑能够持久化。
    """
    test_code = """
class TestClass:
    def test_method(self):
        pass
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        vfs = create_virtual_filesystem(csf)
        
        files = vfs.get_all_files()
        file_path, virtual_file = list(files.items())[0]
        
        # Remove the root prefix to get relative path
        relative_path = file_path.replace(vfs.root_path + '/', '')
        
        original_content = virtual_file.content
        new_content = "# Modified content"
        
        # Edit
        vfs.update_file(relative_path, new_content)
        
        # Verify persistence
        updated = vfs.get_file(relative_path)
        assert updated.content == new_content, "Edit should persist"
        assert updated.content != original_content, "Content should be different"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
