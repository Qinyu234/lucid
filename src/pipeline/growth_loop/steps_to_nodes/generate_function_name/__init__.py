import os
import re

from src.config.load_app_config import load_app_config

from .is_valid_function_name import is_valid_function_name
from .fallback_name import fallback_name


def generate_function_name(node, max_iter=3, job_id=None):

    def _slug_from_semantic(semantic: str) -> str | None:
        words = re.findall(r"[a-zA-Z][a-zA-Z0-9_]{0,30}", semantic.lower())
        if not words:
            return None
        name = "_".join(words[:5])
        if is_valid_function_name(name):
            return name
        return None

    semantic = node.get("semantic", "")
    cfg = load_app_config().get("growth", {})
    use_llm = cfg.get("naming_use_llm", False)

    slug = _slug_from_semantic(semantic)
    if slug:
        return slug

    if not use_llm:
        return fallback_name(semantic)

    from src.llm import llm

    candidate = None
    for _ in range(max_iter):
        prompt = f"""
Convert semantic into a Python-safe function/module name.

Rules:
- snake_case only
- english only
- max 5 words
- must be valid Python identifier
- no explanation, output only name

semantic:
{semantic}
"""
        if candidate:
            prompt += f"\nPrevious invalid attempt:\n{candidate}\nFix it.\n"

        candidate = llm("naming", prompt, job_id=job_id)
        candidate = candidate.strip().replace(" ", "_")

        if is_valid_function_name(candidate):
            return candidate

    return fallback_name(semantic)
