def build_prompt(node):

    from src.schema.io.format_io_comment import format_io_comment

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
- steps: 1 to 4 items
- each io field: name (snake_case) + type (str|int|float|bool|bytes|list|dict|any)
- SEQ: step[i].io.out keys/types must match step[i+1].io.in for shared keys
- tag only for mutually exclusive branches (ROUTER) or parallel/par (PAR)
- DO NOT output code or file paths
"""
