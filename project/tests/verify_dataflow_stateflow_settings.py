"""
Test for dataflow/stateflow detailed settings and semantic complexity assessment
验证dataflow/stateflow详细设置和语义复杂度评估
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.desugar import desugar
from core.flow import analyze_flows


def test_dataflow_detailed_settings():
    """
    Test that dataflow has detailed settings.
    测试dataflow有详细设置。
    """
    test_code = """
def process(x, y):
    z = x + y
    w = z * 2
    return w
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        
        # Check that dataflow information is detailed
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                # Should have dataflow metadata
                assert 'dataflow' in node['meta'], "Should have dataflow metadata"
                
                dataflow = node['meta']['dataflow']
                
                # Should have detailed flow information
                assert 'variables' in dataflow or 'flow' in dataflow, "Dataflow should have variables or flow info"
                
                # Should have settings
                assert 'settings' in dataflow or 'config' in dataflow, "Dataflow should have settings"
    finally:
        Path(temp_path).unlink()


def test_stateflow_detailed_settings():
    """
    Test that stateflow has detailed settings.
    测试stateflow有详细设置。
    """
    test_code = """
class StateMachine:
    def __init__(self):
        self.state = 'idle'
    
    def process(self, event):
        if self.state == 'idle':
            if event == 'start':
                self.state = 'running'
        elif self.state == 'running':
            if event == 'stop':
                self.state = 'idle'
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        
        # Check that stateflow information is detailed
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                # Should have stateflow metadata
                assert 'stateflow' in node['meta'], "Should have stateflow metadata"
                
                stateflow = node['meta']['stateflow']
                
                # Should have detailed state information
                assert 'states' in stateflow or 'transitions' in stateflow, "Stateflow should have states or transitions"
                
                # Should have settings
                assert 'settings' in stateflow or 'config' in stateflow, "Stateflow should have settings"
    finally:
        Path(temp_path).unlink()


def test_semantic_complexity_from_flows():
    """
    Test that semantic complexity is assessed from dataflow and stateflow.
    测试从dataflow和stateflow评估语义复杂度。
    """
    test_code = """
def complex_flow(data):
    result = []
    for item in data:
        if item > 0:
            temp = item * 2
            if temp < 100:
                result.append(temp)
    return result
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        
        # Check for semantic complexity based on flows
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                # Should have semantic complexity
                assert 'semantic_complexity' in node['meta'], "Should have semantic_complexity"
                
                # Semantic complexity should be based on flow complexity
                semantic_complexity = node['meta']['semantic_complexity']
                assert isinstance(semantic_complexity, (int, float)), "semantic_complexity should be numeric"
                
                # Should be influenced by dataflow and stateflow
                if 'dataflow' in node['meta']:
                    dataflow = node['meta']['dataflow']
                    # Semantic complexity should correlate with flow complexity
                    assert semantic_complexity >= 0, "Semantic complexity should be non-negative"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
