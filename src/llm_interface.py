# =========================
# FUNCTION: LLM Interface
# PURPOSE:
# Expand active tree nodes using Qwen coder
# =========================

from .llm import generate


def traverse_and_fill(tree,llm):

    root=tree["root"]

    queue=[root]

    while queue:

        node=queue.pop()

        if node.completed:
            continue

        prompt=build_prompt(node)

        code=generate(prompt)

        node.update_code(
            node.code+"\n"+code
        )

        node.mark_completed()

        queue.extend(
            node.children
        )


def build_prompt(node):

    return f"""
semantic:

{node.semantic}

current code:

{node.code}

continue implementation

only output code
"""