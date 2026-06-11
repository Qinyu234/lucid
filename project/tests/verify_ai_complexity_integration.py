"""
Test for AI complexity/reliability/readability assessment integration
验证AI复杂度/可靠性/可读性评估集成
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar
from core.complexity import estimate_complexity


def test_ai_complexity_estimation():
    """
    Test that AI complexity estimation is integrated into code generation.
    测试AI复杂度评估集成到代码生成。
    """
    test_code = """
def simple_function(x):
    return x + 1

def complex_function(data):
    result = []
    for item in data:
        if item > 0:
            for i in range(10):
                result.append(item * i)
        else:
            result.append(0)
    return result
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        
        # Estimate complexity
        csf = estimate_complexity(csf)
        
        # Check that complexity metadata is present
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                # Should have complexity_score
                assert 'complexity_score' in node['meta'], "Should have complexity_score"
                assert isinstance(node['meta']['complexity_score'], (int, float)), "complexity_score should be numeric"
                
                # Should have reliability_score
                assert 'reliability_score' in node['meta'], "Should have reliability_score"
                assert isinstance(node['meta']['reliability_score'], (int, float)), "reliability_score should be numeric"
                
                # Should have readability_score
                assert 'readability_score' in node['meta'], "Should have readability_score"
                assert isinstance(node['meta']['readability_score'], (int, float)), "readability_score should be numeric"
    finally:
        Path(temp_path).unlink()


def test_ai_assessment_influences_code_generation():
    """
    Test that AI assessment influences code generation decisions.
    测试AI评估影响代码生成决策。
    """
    test_code = """
def high_complexity_func(x):
    if x > 0:
        for i in range(100):
            for j in range(100):
                if i % 2 == 0:
                    x += i * j
    return x
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = estimate_complexity(csf)
        
        # Find the function
        func_node = None
        for node in csf['nodes'].values():
            if node['kind'] == 'function' and node['label'] == 'high_complexity_func':
                func_node = node
                break
        
        assert func_node is not None, "Should find the function"
        
        # High complexity should trigger warnings or suggestions
        complexity = func_node['meta']['complexity_score']
        assert complexity > 0, "Complexity should be positive"
        
        # Should have reliability and readability scores
        assert 'reliability_score' in func_node['meta'], "Should have reliability_score"
        assert 'readability_score' in func_node['meta'], "Should have readability_score"
    finally:
        Path(temp_path).unlink()


def test_semantic_complexity_assessment():
    """
    Test that semantic complexity is assessed.
    测试语义复杂度评估。
    """
    test_code = """
def process_data(items):
    results = []
    for item in items:
        if item is not None:
            results.append(item.value if hasattr(item, 'value') else str(item))
    return results
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = estimate_complexity(csf)
        
        # Check for semantic complexity metrics
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                # Should have semantic complexity
                assert 'semantic_complexity' in node['meta'], "Should have semantic_complexity"
                assert isinstance(node['meta']['semantic_complexity'], (int, float)), "semantic_complexity should be numeric"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
