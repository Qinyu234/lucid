def build_prompt(node, target_steps: int | None = None, max_steps: int = 4):

    from src.shared.validate.io_format_comment_util import io_format_comment_util

    io = node.get("io") or {}
    io_in, io_out = io_format_comment_util(io)
    max_steps = max(2, min(4, int(max_steps)))
    if target_steps is None:
        count_rule = f"steps: 2 to {max_steps} items (prefer at least 2 for non-trivial tasks)"
    else:
        n = max(2, min(max_steps, int(target_steps)))
        count_rule = f"steps: EXACTLY {n} items (no more, no fewer)"

    return f"""
You are a strict task decomposition engine.
Decompose the CURRENT NODE into 2-4 implementable steps.
Return ONLY JSON (no markdown, no prose).

CURRENT NODE:
semantic: {node.get("semantic")}
io.in: {io_in}
io.out: {io_out}

OUTPUT FORMAT (STRICT JSON ONLY):

{{
  "io": {{
    "in": [{{"name": "key_name", "type": "str"}}],
    "out": [{{"name": "key_name", "type": "str"}}]
  }},
  "steps": [
    {{
      "semantic": "short step description",
      "tag": null,
      "io": {{
        "in": [{{"name": "key_name", "type": "str"}}],
        "out": [{{"name": "key_name", "type": "str"}}]
      }}
    }}
  ]
}}

RULES:
- ONLY return valid JSON, no markdown
- {count_rule}
- each io field: name (snake_case) + type (str|int|float|bool|bytes|list|dict|any)
- name steps like functions (snake_case verbs). Avoid: "util", "helper", "misc", "process", "handle"
- keep each step small (<= 20 lines); split if too complex
- SEQ: step[i].io.out keys/types MUST match step[i+1].io.in for every shared key
- first step io.in should overlap parent io.in; last step io.out should overlap parent io.out
- ROUTER: set distinct tag on each mutually exclusive branch (at least 2 tags)
- PAR: set tag "par" on parallel branches
- DO NOT output code or file paths
"""
