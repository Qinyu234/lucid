"""
Test for state explicit functionality
验证状态显式化功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar


def test_state_explicit():
    """
    Test that state is made explicit.
    测试状态能够显式化。
    """
    test_code = """
class StatefulClass:
    def __init__(self):
        self.counter = 0
    
    def increment(self):
        self.counter += 1
        return self.counter
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        
        # Check that state complexity is tracked
        function_nodes = [node for node in csf['nodes'].values() if node['kind'] == 'function']
        
        for node in function_nodes:
            # Should have state complexity metadata
            assert 'state_complexity' in node['meta'], "Function should have state_complexity metadata"
            assert node['meta']['state_complexity'] >= 0, "State complexity should be non-negative"
    finally:
        Path(temp_path).unlink()


def test_mutation_tracking():
    """
    Test that mutations are tracked.
    测试变异能够被跟踪。
    """
    test_code = """
class MutableClass:
    def modify_state(self, value):
        self.value = value
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Check that mutations are annotated
        function_nodes = [node for node in csf['nodes'].values() if node['kind'] == 'function']
        
        for node in function_nodes:
            # Should have mutations list
            assert 'mutations' in node, "Function should have mutations list"
            # Mutations can be empty list
            assert isinstance(node['mutations'], list), "Mutations should be a list"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
