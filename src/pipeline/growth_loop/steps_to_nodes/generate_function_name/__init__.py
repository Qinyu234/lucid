from src.shared.load_app_config import load_app_config
from .is_valid_function_name import is_valid_function_name
from .fallback_name import fallback_name

def generate_function_name(node, max_iter=3, job_id=None, used_names: set | None=None):
    import os
    import re

    def _slug_from_semantic(semantic: str) -> str | None:
        words = re.findall('[a-zA-Z][a-zA-Z0-9_]{0,30}', semantic.lower())
        if not words:
            return None
        name = '_'.join(words[:5])
        if is_valid_function_name(name):
            return name
        return None
    semantic = node.get('semantic', '')
    cfg = load_app_config().get('growth', {})
    use_llm = cfg.get('naming_use_llm', False)
    slug = _slug_from_semantic(semantic)
    if slug:
        if used_names and slug in used_names:
            idx = 2
            base = slug
            while f'{base}_{idx}' in used_names:
                idx += 1
            return f'{base}_{idx}'
        return slug
    if not use_llm:
        name = fallback_name(semantic)
    else:
        from src.llm import llm
        candidate = None
        name = fallback_name(semantic)
        for _ in range(max_iter):
            prompt = f'\nConvert semantic into a Python-safe function/module name.\n\nRules:\n- snake_case only\n- english only\n- max 5 words\n- must be valid Python identifier\n- no explanation, output only name\n\nsemantic:\n{semantic}\n'
            if candidate:
                prompt += f'\nPrevious invalid attempt:\n{candidate}\nFix it.\n'
            candidate = llm('naming', prompt, job_id=job_id)
            candidate = candidate.strip().replace(' ', '_')
            if is_valid_function_name(candidate):
                name = candidate
                break
    if used_names:
        base = name
        if name in used_names:
            idx = 2
            while f'{base}_{idx}' in used_names:
                idx += 1
            name = f'{base}_{idx}'
    return name
