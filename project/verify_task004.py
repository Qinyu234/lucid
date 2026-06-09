import sys
sys.path.insert(0, 'project')
from pathlib import Path
from core.sync.parser import parse
from core.expansion.inheritance import expand_inheritance

p = Path('project/examples/inherit_sample.py')
p.write_text('''class Animal:
    def speak(self):
        return 'sound'

class Dog(Animal):
    def fetch(self):
        return 'ball'
'''.strip(), encoding='utf-8')

csf = parse(str(p))
csf2 = expand_inheritance(csf)
# Dog should see speak method
dog_node = next(n for n in csf2['nodes'].values()
                if n['kind']=='class' and n['label']=='Dog')
child_ids = dog_node['children']
child_labels = [csf2['nodes'][c]['label'] for c in child_ids]
assert 'speak' in child_labels, f'inherited speak not found: {child_labels}'
speak_node = next(csf2['nodes'][c] for c in child_ids if csf2['nodes'][c]['label']=='speak')
assert speak_node['meta'].get('inherited_from') == 'Animal'
assert speak_node['meta'].get('virtual') == True
print('OK')
