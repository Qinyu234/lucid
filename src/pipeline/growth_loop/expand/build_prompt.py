def build_prompt(node):

    from src.shared.format_io_comment import format_io_comment

    io = node.get("io") or {}
    io_in, io_out = format_io_comment(io)

    return f"""
You are a strict task decomposition engine.

Decompose the CURRENT NODE into at most 4 execution steps.

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
- steps: 2 to 4 items (prefer at least 2 for non-trivial tasks)
- each io field: name (snake_case) + type (str|int|float|bool|bytes|list|dict|any)
- SEQ: step[i].io.out keys/types MUST match step[i+1].io.in for every shared key
- first step io.in should overlap parent io.in; last step io.out should overlap parent io.out
- ROUTER: set distinct tag on each mutually exclusive branch (at least 2 tags)
- PAR: set tag "par" on parallel branches
- DO NOT output code or file paths
"""
