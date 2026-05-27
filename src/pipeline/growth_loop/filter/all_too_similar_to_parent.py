def all_too_similar_to_parent(proposal, parent_semantic, threshold=0.85) -> bool:
    from src.pipeline.growth_loop.filter.evaluate_split import evaluate_split

    valid, reason, _ = evaluate_split(parent_semantic or "", proposal)
    return not valid and reason == "all_steps_similar_to_parent"
