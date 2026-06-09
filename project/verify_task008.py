import sys
sys.path.insert(0, 'project')
from core.expansion import expand

csf = expand('project/examples/frontend_sample.py')
assert 'nodes' in csf
assert len(csf['nodes']) > 0
# Should have virtual nodes (inheritance expansion)
virtual = [n for n in csf['nodes'].values() if n.get('meta',{}).get('virtual')]
print(f'nodes={len(csf["nodes"])} virtual={len(virtual)}')
print('OK')
