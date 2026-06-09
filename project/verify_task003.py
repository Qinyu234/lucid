import sys
sys.path.insert(0, 'project')
from pathlib import Path
from core.sync.parser import parse

p = Path('project/examples/frontend_sample.py')
p.parent.mkdir(exist_ok=True)
p.write_text('''class UserService:
    def login(self, token):
        user = self.validate(token)
        if user:
            self.cache[token] = user
        return user

    def validate(self, token):
        return token == "secret"
'''.strip(), encoding='utf-8')

csf = parse(str(p))
assert 'nodes' in csf
kinds = [n['kind'] for n in csf['nodes'].values()]
assert 'class' in kinds
assert 'function' in kinds
assert 'block' in kinds
print(f'nodes={len(csf["nodes"])}')
print('OK')
