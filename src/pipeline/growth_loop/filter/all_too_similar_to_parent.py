from .evaluate_split import evaluate_split


def all_too_similar_to_parent(proposal, parent_semantic, threshold=0.85) -> bool:
    valid, reason, _ = evaluate_split(parent_semantic or "", proposal)
    return not valid and reason == "all_steps_similar_to_parent"
