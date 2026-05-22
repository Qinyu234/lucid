from pathlib import Path

from src.config import load_app_config

from .context_builder import context_builder


def build_prompt(node):

    context = context_builder(node)
    cfg = load_app_config()
    shared = Path(cfg.get("shared_dir", "io/output/shared")).name

    return f"""
You are generating a Python leaf module.

TASK:
{context["semantic"]}

DATAFLOW (ctx):
- read ctx["data"] keys: {context["io_in"]}
- write ctx["data"] keys: {context["io_out"]}

IMPORT RULES (STRICT):
- stdlib only, OR from {shared}.<module> import ...
- NO relative imports
- NO importing other project packages or sibling modules

CODE RULES:
- Output ONLY valid Python
- Exactly ONE function: def run(ctx): ...
- Only imports + run(), nothing else at module level
- Use ctx.get("data", {{}}) and ctx.get("state", {{}})
- Return ctx
- No if __name__ == "__main__"
"""
