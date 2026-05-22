def build_prompt(node):

        return f"""
You are a strict decomposition engine.

You MUST decompose the given node into IPO structure.

CURRENT NODE:
{node}

OUTPUT FORMAT (STRICT JSON ONLY):

{{
  "input": [],
  "process": [],
  "output": []
}}

RULES:
- ONLY return valid JSON
- DO NOT output explanations
- DO NOT output markdown
- Each field must be a list of short semantic fragments
- Do NOT generate code or file paths
- Keep items minimal and atomic
"""
