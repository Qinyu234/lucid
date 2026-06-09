import sys
sys.path.insert(0, 'project')
from pathlib import Path
from core.sync.parser import parse
from core.expansion.nesting import flatten_nesting

p = Path('project/examples/nesting_sample.py')
p.write_text('''def deep_nested():
    if a:
        for b in items:
            if c:
                while d:
                    pass
'''.strip(), encoding='utf-8')

csf = parse(str(p))
csf2 = flatten_nesting(csf, max_depth=3)
# Deepest block should be marked
deep_nodes = [n for n in csf2['nodes'].values()
              if n.get('meta',{}).get('suggest_extraction')]
assert len(deep_nodes) > 0, 'no deep nodes marked'
print(f'suggest_extraction: {len(deep_nodes)} nodes')
print('OK')
