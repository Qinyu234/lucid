from .call_llm import call_llm
from .is_valid_function_name import is_valid_function_name
from .fallback_name import fallback_name

def generate_function_name(node, max_iter=3):

    semantic = node["semantic"]

    candidate = None

    for i in range(max_iter):

        # =========================
        # prompt includes previous failure
        # =========================

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

        candidate = call_llm(prompt)

        candidate = candidate.strip().replace(" ", "_")

        # =========================
        # strict validation
        # =========================

        if is_valid_function_name(candidate):
            return candidate

    # =========================
    # fallback (guaranteed safe)
    # =========================

    return fallback_name(semantic)