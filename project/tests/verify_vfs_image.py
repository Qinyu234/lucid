"""
Test for image virtual file functionality
验证图像虚拟文件功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.vfs.image_virtual import ImageVirtualFile, create_flowchart_image
from core.expansion import expand
from core.desugar import desugar


def test_image_virtual_file():
    """
    Test that images can be created as virtual files.
    测试图像能够作为虚拟文件创建。
    """
    # Create an image virtual file
    image_file = ImageVirtualFile("test_image.png", image_format="png")
    
    assert image_file is not None, "Should create image virtual file"
    assert image_file.file_type == "image", "Should be image type"
    assert image_file.image_format == "png", "Should have correct format"


def test_image_file_metadata():
    """
    Test that image files have proper metadata.
    测试图像文件有正确的元数据。
    """
    image_file = ImageVirtualFile("test.png", image_format="png")
    
    # Set complexity score
    image_file.set_complexity_score(0.5)
    
    # Check metadata
    assert image_file.get_metadata('complexity_score') == 0.5, "Should have complexity_score metadata"
    assert image_file.image_format == "png", "Should have format"


def test_flowchart_image_creation():
    """
    Test that flowchart images can be created from CSF.
    测试能够从CSF创建流程图图像。
    """
    test_code = """
def simple_func():
    return 42
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Create flowchart image
        image_file = create_flowchart_image("flowchart.svg", csf)
        
        assert image_file is not None, "Should create flowchart image"
        assert image_file.file_type == "image", "Should be image type"
        assert image_file.image_format == "svg", "Should be SVG format"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
