def all_too_similar_to_parent(proposal, parent_semantic, threshold=0.85) -> bool:
    from src.shared.lib.all_too_similar_util import all_too_similar_util

    return all_too_similar_util(proposal, parent_semantic, threshold)
