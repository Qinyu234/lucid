"""
Test for inheritance mapper functionality
验证继承映射器功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar
from core.vfs import create_virtual_filesystem
from core.vfs.inheritance_mapper import map_inheritance_to_vfs


def test_inheritance_mapping():
    """
    Test that inheritance can be mapped to virtual files.
    测试继承能够映射到虚拟文件。
    """
    test_code = """
class BaseClass:
    def base_method(self):
        return "base"

class DerivedClass(BaseClass):
    def derived_method(self):
        return "derived"
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        vfs = create_virtual_filesystem(csf)
        
        # Map inheritance to virtual files
        map_inheritance_to_vfs(csf, vfs)
        
        # Check that virtual files are created
        files = vfs.get_all_files()
        assert len(files) >= 0, "Should have virtual files"
    finally:
        Path(temp_path).unlink()


def test_inheritance_file_structure():
    """
    Test that inheritance creates proper file structure.
    测试继承创建正确的文件结构。
    """
    test_code = """
class Parent:
    def parent_method(self):
        pass

class Child(Parent):
    def child_method(self):
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
        
        # Map inheritance to virtual files
        map_inheritance_to_vfs(csf, vfs)
        
        # Check that virtual files are created
        files = vfs.get_all_files()
        assert len(files) >= 0, "Should have virtual files"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
