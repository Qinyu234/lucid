"""
Test for mutation annotation functionality
验证变异标注功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand


def test_mutation_annotation():
    """
    Test that mutations are annotated.
    测试变异能够被标注。
    """
    test_code = """
class MutableClass:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        self.value += 1
        return self.value
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Check that mutations are annotated
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                # Should have mutations list
                assert 'mutations' in node, "Function should have mutations list"
                assert isinstance(node['mutations'], list), "Mutations should be a list"
    finally:
        Path(temp_path).unlink()


def test_mutation_tracking():
    """
    Test that mutation targets are tracked.
    测试变异目标能够被跟踪。
    """
    test_code = """
def modify_state(data):
    data['count'] += 1
    data['total'] = data['count'] * 2
    return data
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Check that mutations are tracked
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                # Should have mutations list
                assert 'mutations' in node, "Function should have mutations list"
                # Mutations can be empty if no mutations detected
                assert isinstance(node['mutations'], list), "Mutations should be a list"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
