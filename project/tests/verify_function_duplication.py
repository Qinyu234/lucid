"""
Test for function duplication functionality
验证函数重复功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.expansion.deduplication import duplicate_function, get_reuse_candidates, deduplicate_functions


def test_function_duplication():
    """
    Test that functions can be duplicated.
    测试函数能够被重复。
    """
    test_code = """
def original():
    return 42
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Find original function
        original_id = None
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function' and node['label'] == 'original':
                original_id = node_id
                break
        
        if original_id:
            # Duplicate function
            new_id = duplicate_function(csf, original_id, 'duplicate')
            
            assert new_id is not None, "Should duplicate function"
            assert new_id in csf['nodes'], "New node should be in CSF"
            assert csf['nodes'][new_id]['label'] == 'duplicate', "New function should have new name"
        
        assert csf is not None, "CSF should exist"
    finally:
        Path(temp_path).unlink()


def test_reuse_candidates():
    """
    Test that reuse candidates can be identified.
    测试重用候选者能够被识别。
    """
    test_code = """
def helper():
    return 1

def a():
    return helper()

def b():
    return helper()

def c():
    return helper()
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Get reuse candidates
        candidates = get_reuse_candidates(csf, min_reuse_count=2)
        
        assert candidates is not None, "Should get reuse candidates"
        assert len(candidates) > 0, "Should have at least one candidate"
        
        # Helper should be a candidate (used 3 times)
        helper_found = any(c['label'] == 'helper' for c in candidates)
        assert helper_found, "Helper should be a reuse candidate"
    finally:
        Path(temp_path).unlink()


def test_multi_round_deduplication():
    """
    Test that multi-round deduplication works.
    测试多轮去重工作。
    """
    test_code = """
def func():
    return 1

def func():
    return 1

def func():
    return 1
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        
        # Count functions before deduplication
        func_count_before = sum(1 for n in csf['nodes'].values() if n['kind'] == 'function')
        
        # Deduplicate with multiple rounds
        csf = deduplicate_functions(csf, max_rounds=3)
        
        # Count functions after deduplication
        func_count_after = sum(1 for n in csf['nodes'].values() if n['kind'] == 'function')
        
        assert func_count_after < func_count_before, "Should reduce function count"
        assert func_count_after == 1, "Should have only one function after deduplication"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
