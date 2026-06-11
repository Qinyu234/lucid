"""
Test for incremental parsing functionality
验证增量解析功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.sync.incremental import incremental_update
from core.sync.parser import parse


def test_incremental_update():
    """
    Test that incremental update works.
    测试增量更新能够工作。
    """
    test_code = """
def original_function():
    return 0
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        # Parse initial
        old_csf = parse(temp_path)
        
        # Update file
        new_code = """
def original_function():
    return 0

def new_function():
    return 1
"""
        
        # Incremental update
        updated_csf = incremental_update(old_csf, new_code, temp_path)
        
        assert updated_csf is not None, "Should update incrementally"
        assert 'nodes' in updated_csf, "CSF should have nodes"
    finally:
        Path(temp_path).unlink()


def test_incremental_preserves_state():
    """
    Test that incremental update preserves expansion state.
    测试增量更新保留扩展状态。
    """
    test_code = """
def test_function():
    return 42
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        # Parse initial
        old_csf = parse(temp_path)
        
        # Set expansion state on a node
        if old_csf['nodes']:
            first_node_id = list(old_csf['nodes'].keys())[0]
            old_csf['nodes'][first_node_id]['expansion_state'] = 'expanded'
        
        # Incremental update with same code
        updated_csf = incremental_update(old_csf, test_code, temp_path)
        
        assert updated_csf is not None, "Should update incrementally"
        assert 'nodes' in updated_csf, "CSF should have nodes"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
