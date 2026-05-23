from .evaluate_split import evaluate_split


def filter(proposal, parent_semantic=None):
    valid, _, accepted = evaluate_split(parent_semantic or "", proposal)
    return accepted if valid else []
