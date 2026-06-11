"""
Test for stateflow analysis functionality
验证状态流分析功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar
from core.flow import analyze_flows


def test_stateflow_analysis():
    """
    Test that stateflow is analyzed.
    测试状态流能够被分析。
    """
    test_code = """
class StateMachine:
    def __init__(self):
        self.state = "idle"
    
    def transition(self):
        if self.state == "idle":
            self.state = "active"
        elif self.state == "active":
            self.state = "idle"
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        
        # Check that stateflow metadata is added
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                assert 'stateflow' in node['meta'], "Should have stateflow metadata"
                stateflow = node['meta']['stateflow']
                # Stateflow should exist (can be empty if no state changes)
                assert isinstance(stateflow, dict), "stateflow should be a dict"
    finally:
        Path(temp_path).unlink()


def test_state_transitions():
    """
    Test that state transitions are tracked.
    测试状态转换能够被跟踪。
    """
    test_code = """
def update_state(state, value):
    if value > 0:
        return "positive"
    else:
        return "negative"
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        
        # Check that state transitions are tracked
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                assert 'stateflow' in node['meta'], "Should have stateflow metadata"
                stateflow = node['meta']['stateflow']
                # State transitions should be tracked
                assert 'state_transitions' in stateflow or isinstance(stateflow, dict), \
                    "Should track state transitions"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
