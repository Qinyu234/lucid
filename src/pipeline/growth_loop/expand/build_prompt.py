def build_prompt(node):

    io = node.get("io") or {}

    return f"""
You are a strict task decomposition engine.

Decompose the CURRENT NODE into at most 4 execution steps.

CURRENT NODE:
semantic: {node.get("semantic")}
io.in: {io.get("in", [])}
io.out: {io.get("out", [])}

OUTPUT FORMAT (STRICT JSON ONLY):

{{
  "io": {{ "in": [], "out": [] }},
  "steps": [
    {{
      "semantic": "short step description",
      "tag": null,
      "io": {{ "in": [], "out": [] }}
    }}
  ]
}}

RULES:
- ONLY return valid JSON, no markdown
- steps: 1 to 4 items
- each step needs io.in and io.out (snake_case key names in ctx data)
- sequential steps: step[i].io.out should overlap step[i+1].io.in
- tag only for mutually exclusive branches; all tagged must be unique
- DO NOT output code, paths, or topology names
"""
