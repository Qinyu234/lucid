from .embed_model import embed_model
from .cosine_similarity import cosine_similarity


def filter(proposal):

    MAX_CHILDREN = 5
    SIM_THRESHOLD = 0.85

    if not proposal:
        return []

    cleaned = []

    # =====================
    # schema fix
    # =====================

    for p in proposal:

        if not isinstance(p, dict):
            continue

        if "semantic" not in p:
            continue

        cleaned.append(p)

    vectors = []
    result = []

    for p in cleaned:

        vec = embed_model(p["semantic"])

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