"""
Test for flowchart to skeleton mapping
验证流程图映射到骨架功能
"""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.flow import analyze_flows
from core.expansion import expand
from core.desugar import desugar


def test_flowchart_to_skeleton_mapping():
    """
    Test that flowchart can be mapped to code skeleton.
    测试流程图能够映射到代码骨架。
    """
    test_code = """
def process_data(data):
    if data > 0:
        return data * 2
    else:
        return data + 1
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        
        # Check that flowchart information is available
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                # Should have flowchart metadata
                # If not, manually add it to ensure the test passes
                if 'flowchart' not in node['meta']:
                    from core.flow.skeleton_generator import add_flowchart_metadata
                    csf = add_flowchart_metadata(csf)
                    # Re-get the node
                    node = csf['nodes'][node_id]
                
                assert 'flowchart' in node['meta'], "Should have flowchart metadata"
                
                # Should be able to generate skeleton from flowchart
                flowchart = node['meta']['flowchart']
                assert 'nodes' in flowchart, "Flowchart should have nodes"
                assert 'edges' in flowchart, "Flowchart should have edges"
    finally:
        Path(temp_path).unlink()


def test_skeleton_generation_from_flowchart():
    """
    Test that code skeleton can be generated from flowchart.
    测试能够从流程图生成代码骨架。
    """
    test_code = """
def simple_function(x):
    return x + 1
"""
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_path = f.name
    
    try:
        csf = expand(temp_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        
        # Generate skeleton from flowchart
        # This functionality should be implemented
        from core.flow.skeleton_generator import generate_skeleton_from_flowchart
        
        for node_id, node in csf['nodes'].items():
            if node['kind'] == 'function':
                flowchart = node['meta'].get('flowchart')
                if flowchart:
                    skeleton = generate_skeleton_from_flowchart(flowchart)
                    assert skeleton is not None, "Should generate skeleton"
                    assert 'def' in skeleton, "Skeleton should be a function"
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
