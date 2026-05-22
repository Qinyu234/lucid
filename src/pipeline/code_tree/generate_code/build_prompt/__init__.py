from .context_builder import context_builder

def build_prompt(node):

    context = context_builder(node)

    is_interface = context["children_count"] > 0

    if is_interface:

        return f"""
You are generating a Python package interface (__init__.py).

TASK:
{context["semantic"]}

CONTEXT:
- This module aggregates {context["children_count"]} submodules

RULES:
- exactly one function named __init__
"""

    return f"""
You are generating a Python function.

TASK:
{context["semantic"]}

CONTEXT:
- Leaf implementation node

RULES:
- exactly one function
- no classes
"""