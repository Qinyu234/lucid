from src.config.load_app_config import load_app_config

from .embed_model import embed_model
from .cosine_similarity import cosine_similarity

MAX_CHILDREN = 4


def evaluate_split(parent_semantic: str, proposal: list) -> tuple:
    """
    Decide whether LLM split is valid.

    1) LLM proposes steps (caller)
    2) If embeddings are too similar to parent -> invalid, do NOT split
    3) If valid -> return deduped children for topology attach

    Returns:
        (valid, reason, accepted_proposal)
    """

    def _threshold() -> float:
        cfg = load_app_config().get("growth", {})
        return float(cfg.get("similarity_threshold", 0.85))

    def _proposal_items(proposal: list) -> list:
        return [p for p in proposal if isinstance(p, dict) and p.get("semantic")]

    def _dedupe_siblings(items: list, threshold: float | None = None) -> list:
        threshold = threshold or _threshold()
        vectors = []
        result = []

        for p in items:
            vec = embed_model(p["semantic"])
            if any(cosine_similarity(vec, v) > threshold for v in vectors):
                continue
            vectors.append(vec)
            result.append(p)

        return result

    items = _proposal_items(proposal)
    if not items:
        return False, "empty_proposal", []

    if not parent_semantic:
        return True, "ok", _dedupe_siblings(items)

    threshold = _threshold()
    parent_vec = embed_model(str(parent_semantic))

    scored = []
    for p in items:
        vec = embed_model(p["semantic"])
        sim = cosine_similarity(vec, parent_vec)
        scored.append((p, vec, sim))

    if all(sim > threshold for _, _, sim in scored):
        return False, "all_steps_similar_to_parent", []

    distinct = [p for p, _, sim in scored if sim <= threshold]
    if not distinct:
        return False, "no_distinct_steps", []

    accepted = _dedupe_siblings(distinct, threshold)
    if not accepted:
        return False, "siblings_collapsed", []

    return True, "ok", accepted[:MAX_CHILDREN]
