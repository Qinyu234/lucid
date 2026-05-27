def hybrid_retrieve(query_semantic: str, top_k: int | None = None) -> list:
    from src.shared.lib.app_config_util import app_config_util
    from src.shared.lib.cosine_similarity_util import cosine_similarity_util
    from src.shared.lib.embed_model_util import embed_model_util

    from .extract_keywords import extract_keywords
    from .keyword_score import keyword_score
    from .load_entries import load_entries

    cfg = app_config_util().get("memory", {})
    top_k = top_k or int(cfg.get("retrieve_top_k", 10))
    kw_weight = float(cfg.get("keyword_weight", 0.35))
    emb_weight = float(cfg.get("embedding_weight", 0.65))
    emb_min = float(cfg.get("embedding_min_score", 0.4))
    query_kw = extract_keywords(query_semantic)
    query_vec = embed_model_util(query_semantic)
    scored = []
    for entry in load_entries():
        semantic = entry.get("semantic", "")
        entry_kw = entry.get("keywords") or extract_keywords(semantic)
        kw_s = keyword_score(query_kw, entry_kw)
        emb_s = float(cosine_similarity_util(query_vec, embed_model_util(semantic)))
        combined = kw_weight * kw_s + emb_weight * emb_s
        if emb_s < emb_min and kw_s == 0:
            continue
        item = dict(entry)
        item["_kw_score"] = kw_s
        item["_emb_score"] = emb_s
        item["_retrieve_score"] = combined
        scored.append(item)
    scored.sort(key=lambda x: x["_retrieve_score"], reverse=True)
    return scored[:top_k]
