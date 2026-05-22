from src.llm import call_llm

from .is_valid_function_name import is_valid_function_name
from .fallback_name import fallback_name


def generate_function_name(node, max_iter=3, job_id=None):

    semantic = node["semantic"]
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
            prompt += f"""

Previous invalid attempt:
{candidate}

Fix it and output a valid name.
"""

        candidate = call_llm("naming", prompt, job_id=job_id)
        candidate = candidate.strip().replace(" ", "_")

        if is_valid_function_name(candidate):
            return candidate

    return fallback_name(semantic)
