from src.schema.io.format_io_comment import format_io_comment





def render_reuse_wrapper(node: dict, shared_module: str) -> str:

    fn = node.get("function_name") or "module"

    io_in, io_out = format_io_comment(node.get("io"))

    return (

        f"# semantic: {node.get('semantic', '')}\n"

        f"# io.in: {io_in}\n"

        f"# io.out: {io_out}\n\n"

        f"from shared.{shared_module} import {shared_module}\n\n\n"

        f"def {fn}(ctx):\n"

        f"    return {shared_module}(ctx)\n"

    )


