"""
Test for class to function desugaring
验证类转函数去糖化功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar


def test_class_to_function_conversion():
    """
    Test that classes are converted to functions.
    测试类能够转换为函数。
    """
    test_code = """
class MyClass:
    def my_method(self, x):
        return x + 1
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        
        # After desugaring, should have constructor function
        function_nodes = [node for node in csf['nodes'].values() if node['kind'] == 'function']
        assert len(function_nodes) >= 1, "Should have at least 1 function after desugaring"
        
        # Check for constructor
        constructor_nodes = [node for node in function_nodes if node['meta'].get('is_constructor')]
        assert len(constructor_nodes) >= 1, "Should have constructor function"
        
        # Check for method function
        method_nodes = [node for node in function_nodes if node['meta'].get('desugared_from') == 'method']
        assert len(method_nodes) >= 1, "Should have method function"
    finally:
        Path(temp_path).unlink()


def test_explicit_self_parameter():
    """
    Test that methods have explicit self parameter after desugaring.
    测试去糖化后方法有显式的self参数。
    """
    test_code = """
class TestClass:
    def test_method(self, value):
        return value * 2
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        
        # Check that method functions have self_parameter metadata
        function_nodes = [node for node in csf['nodes'].values() if node['kind'] == 'function']
        method_nodes = [node for node in function_nodes if node['meta'].get('desugared_from') == 'method']
        
        for method in method_nodes:
            assert 'self_parameter' in method['meta'], "Method should have self_parameter metadata"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
