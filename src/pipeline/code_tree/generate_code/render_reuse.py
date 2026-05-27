def render_reuse(node, module):
    from src.pipeline.memory import render_reuse_wrapper

    return render_reuse_wrapper(node, module)
