def evaluate_split_bridge(parent_semantic, proposal):
    from src.pipeline.growth_loop.filter import evaluate_split

    return evaluate_split(parent_semantic, proposal)
