from src.config import load_app_config
from src.pipeline.growth_loop.filter.embed_model import embed_model
from src.pipeline.growth_loop.filter.cosine_similarity import cosine_similarity

from .keywords import extract_keywords, keyword_score
from .store import load_entries


def _memory_cfg() -> dict:
    return load_app_config().get("memory", {})


def hybrid_retrieve(query_semantic: str, top_k: int | None = None) -> list:

    cfg = _memory_cfg()
    top_k = top_k or int(cfg.get("retrieve_top_k", 10))
    kw_weight = float(cfg.get("keyword_weight", 0.35))
    emb_weight = float(cfg.get("embedding_weight", 0.65))
    emb_min = float(cfg.get("embedding_min_score", 0.4))

    query_kw = extract_keywords(query_semantic)
    query_vec = embed_model(query_semantic)

    scored = []

    for entry in load_entries():
        semantic = entry.get("semantic", "")
        entry_kw = entry.get("keywords") or extract_keywords(semantic)
        kw_s = keyword_score(query_kw, entry_kw)
        emb_s = cosine_similarity(query_vec, embed_model(semantic))
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
