def render_reuse_wrapper(node: dict, shared_module: str) -> str:
    from src.shared.format_io_comment import format_io_comment
    fn = node.get('function_name') or 'module'
    io_in, io_out = format_io_comment(node.get('io'))
    return f"# semantic: {node.get('semantic', '')}\n# io.in: {io_in}\n# io.out: {io_out}\n\nfrom src.shared.{shared_module} import {shared_module}\n\n\ndef {fn}(ctx):\n    return {shared_module}(ctx)\n"
