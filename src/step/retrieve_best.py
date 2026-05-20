import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def retrieve_best(semantic: str, memory: list, embed_fn, threshold=0.75):
    if not memory:
        return None

    query_vec = embed_fn(semantic).reshape(1, -1)

    best = None
    best_score = 0.0

    for item in memory:
        if "embedding" not in item:
            continue

        mem_vec = np.array(item["embedding"]).reshape(1, -1)

        score = cosine_similarity(query_vec, mem_vec)[0][0]

        if score > best_score:
            best_score = score
            best = item

    if best is None:
        return None

    if best_score < threshold:
        return None

    return best.get("task")