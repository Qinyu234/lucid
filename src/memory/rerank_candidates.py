from src.config.load_app_config import load_app_config


def rerank_candidates(query_semantic: str, candidates: list) -> list:

    _reranker = None

    def _get_reranker():
        nonlocal _reranker
        if _reranker is None:
            from sentence_transformers import CrossEncoder

            cfg = load_app_config()
            model_name = cfg.get(
                "memory_reranker_model",
                "cross-encoder/ms-marco-MiniLM-L-6-v2",
            )
            _reranker = CrossEncoder(model_name)
        return _reranker

    if not candidates:
        return []

    cfg = load_app_config().get("memory", {})
    top_k = int(cfg.get("rerank_top_k", 5))
    min_score = float(cfg.get("rerank_min_score", -2.0))

    reranker = _get_reranker()
    pairs = [[query_semantic, c.get("semantic", "")] for c in candidates]
    scores = reranker.predict(pairs)

    ranked = []
    for cand, score in zip(candidates, scores):
        item = dict(cand)
        item["_rerank_score"] = float(score)
        if item["_rerank_score"] >= min_score:
            ranked.append(item)

    ranked.sort(key=lambda x: x["_rerank_score"], reverse=True)
    return ranked[:top_k]
