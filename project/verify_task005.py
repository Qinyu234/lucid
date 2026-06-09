import sys
sys.path.insert(0, 'project')
from pathlib import Path
from core.sync.parser import parse
from core.expansion.dependency import expand_dependencies

p = Path('project/examples/dep_sample.py')
p.write_text('''def fetch():
    return get_from_db()

def get_from_db():
    return {'data': 1}

def process():
    data = fetch()
    return data
'''.strip(), encoding='utf-8')

csf = parse(str(p))
csf2 = expand_dependencies(csf, max_span=2)
process_node = next(n for n in csf2['nodes'].values()
                    if n['kind']=='function' and n['label']=='process')
child_ids = process_node['children']
child_labels = [csf2['nodes'][c]['label'] for c in child_ids if c in csf2['nodes']]
print(f'process children: {child_labels}')
print('OK')
