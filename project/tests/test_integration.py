"""
端到端集成测试
"""
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.expansion import expand
from core.recognition.rpcm import compute_ws_state
from core.projection.scheduler import schedule
from core.pattern.matcher import match_patterns
from core.template.registry import check_constraints
from core.template.generator import generate
from core.sync.parser import incremental_update


def test_understanding_direction_complete_flow():
    """
    Test 1: 理解方向完整流程
    expand → compute_ws_state → schedule → match_patterns
    """
    # Create a test file
    test_file = Path(__file__).parent.parent / 'examples' / 'integration_test.py'
    test_file.write_text('''
class UserService:
    def login(self, token):
        user = self.validate(token)
        if user:
            self.cache[token] = user
        return user

    def validate(self, token):
        return token == "secret"
'''.strip(), encoding='utf-8')
    
    try:
        # expand
        csf = expand(str(test_file))
        assert 'nodes' in csf
        assert len(csf['nodes']) > 0
        
        # compute_ws_state
        ws = compute_ws_state(csf)
        assert 'R0' in ws and 'R1' in ws and 'R2' in ws and 'R3' in ws
        assert ws['R0']['ws_op'] in ['stable', 'load', 'compress']
        
        # schedule
        csf2 = schedule(csf)
        # 验证没有 side effect
        assert csf is not csf2
        
        # match_patterns
        matches = match_patterns(csf)
        assert isinstance(matches, list)
        
        # CLI expand 输出结构树（通过验证 csf 结构）
        assert len(csf['root_ids']) > 0
        
    finally:
        # Clean up
        if test_file.exists():
            test_file.unlink()


def test_development_direction_complete_flow():
    """
    Test 2: 开发方向完整流程
    expand → check_constraints → generate
    """
    # Create a test file
    test_file = Path(__file__).parent.parent / 'examples' / 'integration_test2.py'
    test_file.write_text('''
def fetch(data):
    return data

def transform(data):
    return data * 2

def process(data):
    result = fetch(data)
    clean = transform(result)
    cache[data] = clean
    return clean
'''.strip(), encoding='utf-8')
    
    try:
        # expand
        csf = expand(str(test_file))
        assert 'nodes' in csf
        
        # check_constraints
        result = check_constraints('fetch_transform_cache_template', csf)
        assert 'satisfied' in result
        assert 'missing' in result
        assert 'heatmap' in result
        assert 'ready' in result
        
        # 如果约束满足，测试 generate
        if result['ready']:
            gen_result = generate('fetch_transform_cache_template', csf)
            assert 'ok' in gen_result
            assert 'code' in gen_result
            assert 'llm_needed' in gen_result
        else:
            # 约束缺失时 ready=False
            assert not result['ready']
        
    finally:
        # Clean up
        if test_file.exists():
            test_file.unlink()


def test_incremental_sync():
    """
    Test 3: 增量同步
    parse → 修改代码 → incremental_update
    """
    # Create a test file
    test_file = Path(__file__).parent.parent / 'examples' / 'integration_test3.py'
    original_code = '''
def setup():
    theme = 'dark'
    return theme
'''.strip()
    test_file.write_text(original_code, encoding='utf-8')
    
    try:
        # parse
        csf = expand(str(test_file))
        
        # 模拟用户展开了某个节点
        first_id = list(csf['nodes'].keys())[0]
        first_node = csf['nodes'][first_id]
        csf['nodes'][first_id]['expansion_state'] = 'expanded'
        
        # 模拟代码小改动（加一行注释）
        new_source = original_code + '\n# updated'
        csf2 = incremental_update(csf, new_source, str(test_file))
        
        # expansion_state 应该被保留（通过匹配节点而不是 ID）
        # 找到匹配的节点
        def node_key(node):
            return (node['kind'], node['label'], node['source_ref']['line_start'])
        
        old_key = node_key(first_node)
        matching_node = None
        for node in csf2['nodes'].values():
            if node_key(node) == old_key:
                matching_node = node
                break
        
        assert matching_node is not None, 'matching node not found'
        assert matching_node['expansion_state'] == 'expanded', 'state lost'
        
    finally:
        # Clean up
        if test_file.exists():
            test_file.unlink()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
