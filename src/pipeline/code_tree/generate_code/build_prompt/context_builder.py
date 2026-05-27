def context_builder(node: dict, root: dict | None=None):
    from src.shared.io_tree.find_parent_util import find_parent_util
    from src.shared.validate.shared_usage_guide_util import shared_usage_guide_util
    from src.shared.validate.io_format_comment_util import io_format_comment_util
    from src.shared.validate.io_format_side_util import io_format_side_util
    from src.shared.validate.io_normalize_util import io_normalize_util
    io = io_normalize_util(node.get('io'))
    io_in_str, io_out_str = io_format_comment_util(io)
    parent = find_parent_util(root, node) if root else None
    fn = node.get('function_name') or 'module'
    used_by = []
    imports_from_template = []
    if parent:
        parent_fn = parent.get('function_name') or 'package'
        used_by.append(f'{parent_fn}/__init__.py imports: from .{fn} import {fn}')
        imports_from_template.append(f'from .{fn} import {fn}')
    shared = 'src.shared'
    return {'semantic': node.get('semantic', ''), 'function_name': fn, 'io_in': io_in_str, 'io_out': io_out_str, 'io_in_fields': io.get('in', []), 'io_out_fields': io.get('out', []), 'parent_semantic': (parent or {}).get('semantic', ''), 'parent_function': (parent or {}).get('function_name', ''), 'parent_topology': (parent or {}).get('topology'), 'parent_io_in': io_format_side_util((parent or {}).get('io') or {}, 'in'), 'parent_io_out': io_format_side_util((parent or {}).get('io') or {}, 'out'), 'used_by': used_by, 'imports_from_template': imports_from_template, 'shared_module_prefix': shared, 'allowed_imports': [f'{shared}.<category>.<module> — categories: logging, validate, lib, io, debug (e.g. {shared}.lib.time_util)'], 'shared_usage_guide': shared_usage_guide_util()}
