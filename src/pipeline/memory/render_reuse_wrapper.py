def render_reuse_wrapper(node: dict, shared_module: str) -> str:
    from src.shared.validate.io_format_comment_util import io_format_comment_util
    fn = node.get('function_name') or 'module'
    io_in, io_out = io_format_comment_util(node.get('io'))
    return f"# semantic: {node.get('semantic', '')}\n# io.in: {io_in}\n# io.out: {io_out}\n\nfrom src.shared.{shared_module} import {shared_module}\n\n\ndef {fn}(ctx):\n    return {shared_module}(ctx)\n"
