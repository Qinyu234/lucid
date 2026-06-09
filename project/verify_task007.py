import sys
sys.path.insert(0, 'project')
from pathlib import Path
from core.sync.parser import parse
from core.expansion.mutation import annotate_mutations

p = Path('project/examples/mutation_sample.py')
p.write_text('''def setup():
    theme = 'dark'
    return theme

def render_header(theme):
    return f'header:{theme}'

def render_sidebar(theme):
    return f'sidebar:{theme}'
'''.strip(), encoding='utf-8')

csf = parse(str(p))
csf2 = annotate_mutations(csf)
# theme is assigned by setup, render_* depend on it
setup_node = next(n for n in csf2['nodes'].values()
                  if n['kind']=='function' and n['label']=='setup')
print(f'setup mutation_affects: {setup_node["mutation_affects"]}')
print('OK')
