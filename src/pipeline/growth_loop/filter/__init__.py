# =========================
# FUNCTION:
# filter
#
# PURPOSE:
# clean + deduplicate + limit growth
#
# INPUT:
# proposal: List[dict]
#
# OUTPUT:
# filtered proposal
# =========================
from .embed_model import embed_model
from .cosine_similarity import cosine_similarity
def filter(proposal):

    # =====================
    # config (internal)
    # =====================

    MAX_CHILDREN = 5
    SIM_THRESHOLD = 0.85

    # embed function (internal)
    def embed(text):
        return embed_model(text)

    # cosine similarity
    def cosine(a, b):
        return cosine_similarity(a, b)

    # =====================
    # 1. guard
    # =====================

    if not proposal:
        return []

    # =====================
    # 2. schema filter
    # =====================

    cleaned = []

    for p in proposal:

        if not isinstance(p, dict):
            continue

        if "transform" not in p:
            continue

        cleaned.append(p)

    # =====================
    # 3. embedding dedup
    # =====================

    vectors = []
    result = []

    for p in cleaned:

        vec = embed(p["transform"])

        duplicate = False

        for v in vectors:

            if cosine(vec, v) > SIM_THRESHOLD:
                duplicate = True
                break

        if duplicate:
            continue

        vectors.append(vec)
        result.append(p)

        # =====================
        # 4. fan-out limit
        # =====================

        if len(result) >= MAX_CHILDREN:
            break

    return result