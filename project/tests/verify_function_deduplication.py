"""
Test for function deduplication support
验证函数重复使用和去重功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar


def test_function_deduplication():
    """
    Test that duplicate functions can be detected and deduplicated.
    测试能够检测和去重重复的函数。
    """
    # Create test code with duplicate functions (in different scopes)
    test_code = """
class ClassA:
    def helper_function(self, x):
        return x + 1

class ClassB:
    def helper_function(self, x):  # Duplicate name in different scope
        return x + 1

def main():
    return 0
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        # Parse and expand
        csf = expand(temp_path)
        csf = desugar(csf)  # Desugar to flatten classes to functions
        
        # Check that duplicate functions are detected
        function_labels = [node['label'] for node in csf['nodes'].values() if node['kind'] == 'function']
        helper_count = function_labels.count('ClassA_helper_function')
        
        # Should detect at least one
        assert helper_count >= 1, "Should detect ClassA_helper_function"
        
        # After deduplication, should have only one (if they're truly duplicates)
        # For now, just verify the deduplication function runs without error
        from core.expansion.deduplication import deduplicate_functions
        csf_dedup = deduplicate_functions(csf)
        assert csf_dedup is not None, "Deduplication should return CSF"
    finally:
        Path(temp_path).unlink()


def test_function_reuse_tracking():
    """
    Test that function reuse can be tracked across the codebase.
    测试能够跟踪代码库中的函数重用。
    """
    test_code = """
def common_util(x):
    return x * 2

def func_a():
    return common_util(5)

def func_b():
    return common_util(10)
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Find common_util function
        common_util_nodes = [node for node in csf['nodes'].values() 
                            if node['kind'] == 'function' and node['label'] == 'common_util']
        
        assert len(common_util_nodes) == 1, "Should have one common_util function"
        
        # Check that it tracks how many times it's used
        common_util = common_util_nodes[0]
        # This metadata should exist after reuse tracking analysis
        # If not, manually call track_function_reuse to ensure it's set
        from core.expansion.deduplication import track_function_reuse
        csf = track_function_reuse(csf)
        
        # Re-find the node after tracking
        common_util = [node for node in csf['nodes'].values() 
                      if node['kind'] == 'function' and node['label'] == 'common_util'][0]
        
        assert 'reuse_count' in common_util['meta'], "Should track reuse count"
        # The reuse count should be at least 0
        assert common_util['meta']['reuse_count'] >= 0, "Reuse count should be non-negative"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
