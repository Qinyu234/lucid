from .build_prompt import build_prompt
from .call_llm import call_llm
from .verify_code import verify_code


def generate_code(node, max_retry=3):

    for _ in range(max_retry):

        # =========================
        # 1. PROMPT (pure semantic)
        # =========================
        prompt = build_prompt(node)

        # =========================
        # 2. LLM execution
        # =========================
        code = call_llm(prompt)

        # =========================
        # 3. VERIFY (node-driven gate)
        # =========================
        if verify_code(code, node):
            return code

    return ""