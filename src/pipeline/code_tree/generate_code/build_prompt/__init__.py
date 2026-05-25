from .context_builder import context_builder


def build_prompt(node, root=None):

    context = context_builder(node, root=root)
    fn = context["function_name"]
    shared = context["shared_module_prefix"]
    algorithm = context["algorithm_module_prefix"]

    used_by_block = "\n".join(f"- {x}" for x in context["used_by"]) or "- (root or standalone leaf)"
    template_imports = "\n".join(f"- {x}" for x in context["imports_from_template"]) or "- none"
    allowed = ", ".join(context["allowed_imports"])

    return f"""
You are generating a Python leaf module.

SEMANTIC:
{context["semantic"]}

PARENT CONTEXT:
- parent module: {context["parent_function"] or "(none)"}
- parent semantic: {context["parent_semantic"] or "(none)"}
- parent topology: {context["parent_topology"] or "(none)"}
- parent io.in: {context["parent_io_in"]}
- parent io.out: {context["parent_io_out"]}

DATA TYPES (ctx["data"], name:type):
- read io.in: {context["io_in"]}
- write io.out: {context["io_out"]}

ALGORITHM LIBRARY (fixed distribution + fixed business ONLY; pick if regime matches):
{context["algorithm_catalog"]}

IMPORT / USED-BY (auto from template, do NOT violate):
- allowed imports: {allowed}
- example: from {algorithm}.encoding.huffman_known_weights import huffman_known_weights
- use algorithm imports ONLY when node semantic/io matches fixed_task on catalog line
- forbidden: relative imports, sibling imports
- this module used by:
{used_by_block}
- parent template already contains:
{template_imports}

OUTPUT FORMAT:
# semantic: {context["semantic"]}
# io.in: {context["io_in"]}
# io.out: {context["io_out"]}

def {fn}(ctx):
    ...

RULES:
- Output ONLY valid Python
- Exactly ONE function named {fn}
- Respect name:type when reading/writing ctx["data"]
- Return ctx
"""
