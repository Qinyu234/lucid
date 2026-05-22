from .embed_model import embed_model
from .cosine_similarity import cosine_similarity


def filter(proposal, parent_semantic=None):

    MAX_CHILDREN = 4
    SIM_THRESHOLD = 0.85

    if not proposal:
        return []

    cleaned = []

    for p in proposal:

        if not isinstance(p, dict):
            continue

        if "semantic" not in p:
            continue

        cleaned.append(p)

    parent_vec = None
    if parent_semantic:
        parent_vec = embed_model(str(parent_semantic))

    vectors = []
    result = []

    for p in cleaned:

        vec = embed_model(p["semantic"])

        if parent_vec is not None:
            if cosine_similarity(vec, parent_vec) > SIM_THRESHOLD:
                continue

        duplicate = False

        for v in vectors:

            if cosine_similarity(vec, v) > SIM_THRESHOLD:
                duplicate = True
                break

        if duplicate:
            continue

        vectors.append(vec)
        result.append(p)

        if len(result) >= MAX_CHILDREN:
            break

    return result


def all_too_similar_to_parent(proposal, parent_semantic, threshold=0.85) -> bool:

    if not proposal or not parent_semantic:
        return False

    parent_vec = embed_model(str(parent_semantic))

    for p in proposal:
        if not isinstance(p, dict) or not p.get("semantic"):
            continue
        vec = embed_model(p["semantic"])
        if cosine_similarity(vec, parent_vec) <= threshold:
            return False

    return True
