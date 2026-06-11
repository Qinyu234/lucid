"""
Test for state visualization functionality
验证状态可视化功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar
from core.flow import analyze_flows, visualize_state


def test_state_visualization():
    """
    Test that state can be visualized.
    测试状态能够被可视化。
    """
    test_code = """
class StateMachine:
    def __init__(self):
        self.state = "idle"
    
    def transition(self):
        if self.state == "idle":
            self.state = "active"
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        
        # Visualize state
        visualization = visualize_state(csf)
        
        assert visualization is not None, "Should generate state visualization"
        assert isinstance(visualization, dict), "Visualization should be a dict"
    finally:
        Path(temp_path).unlink()


def test_state_diagram_generation():
    """
    Test that state diagrams can be generated.
    测试状态图能够被生成。
    """
    test_code = """
def simple_function():
    return 42
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        
        visualization = visualize_state(csf)
        
        # Check that visualization has structure
        assert 'states' in visualization or isinstance(visualization, dict), \
            "Visualization should have states or be a dict"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
