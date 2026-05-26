from .context_builder import context_builder

def build_prompt(node, root=None):
    context = context_builder(node, root=root)
    fn = context['function_name']
    shared = context['shared_module_prefix']
    used_by_block = '\n'.join((f'- {x}' for x in context['used_by'])) or '- (root or standalone leaf)'
    template_imports = '\n'.join((f'- {x}' for x in context['imports_from_template'])) or '- none'
    allowed = ', '.join(context['allowed_imports'])
    return f"""\nYou are generating a Python leaf module for a generated project.\n\nSEMANTIC:\n{context['semantic']}\n\nPARENT CONTEXT:\n- parent module: {context['parent_function'] or '(none)'}\n- parent semantic: {context['parent_semantic'] or '(none)'}\n- parent topology: {context['parent_topology'] or '(none)'}\n- parent io.in: {context['parent_io_in']}\n- parent io.out: {context['parent_io_out']}\n\nDATA TYPES (ctx["data"], name:type):\n- read io.in: {context['io_in']}\n- write io.out: {context['io_out']}\n\nIMPORT / USED-BY (auto from template, do NOT violate):\n- allowed imports: {allowed}\n- example: from {shared}.ctx_util import ctx_util\n- example: from {shared}.logging_util import logging_util\n- forbidden: stdlib direct import, relative imports, subpackages, any non-shared business import (only __init__.py may import children)\n- this module used by:\n{used_by_block}\n- parent template already contains:\n{template_imports}\n\nOUTPUT FORMAT:\n# semantic: {context['semantic']}\n# io.in: {context['io_in']}\n# io.out: {context['io_out']}\n\ndef {fn}(ctx):\n    ...\n\nRULES:\n- Output ONLY valid Python\n- Exactly ONE top-level function named {fn} (same as file stem)\n- Use {shared} helpers for logging/types/ctx init; do not import stdlib in this file\n- Respect name:type when reading/writing ctx["data"]\n- Return ctx\n"""
