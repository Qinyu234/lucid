def evaluate_split(parent_semantic: str, proposal: list) -> tuple:
    max_children = 4
    from src.shared.lib.feature_util import feature_util
    from src.shared.lib.app_config_util import app_config_util
    from src.shared.lib.re_util import re_util
    from src.shared.lib.sentence_transformer_encode_util import sentence_transformer_encode_util
    from src.shared.lib.cosine_similarity_util import cosine_similarity_util
    '\n    Decide whether LLM split is valid.\n\n    split_validation (growth config, or legacy embedding_split feature):\n      - off: keep LLM steps; drop only exact-duplicate sibling semantics\n      - light: token Jaccard overlap (no ML model); never discard entire proposal\n      - embedding: SentenceTransformer similarity (needs RAM)\n    '

    def _growth_cfg() -> dict:
        return app_config_util().get('growth', {})

    def _validation_mode() -> str:
        cfg = _growth_cfg()
        mode = str(cfg.get('split_validation', '') or '').strip().lower()
        if mode in ('off', 'light', 'embedding'):
            return mode
        if feature_util('embedding_split'):
            return 'embedding'
        return 'light'

    def _token_set(text: str) -> set:
        re = re_util()
        return set(re.findall(r"[a-zA-Z0-9_]+|[\u4e00-\u9fff]+", str(text).lower()))

    def _jaccard(a: str, b: str) -> float:
        ta, tb = (_token_set(a), _token_set(b))
        if not ta and (not tb):
            return 1.0
        if not ta or not tb:
            return 0.0
        inter = len(ta & tb)
        union = len(ta | tb)
        return inter / union if union else 0.0

    def _threshold() -> float:
        return float(_growth_cfg().get('similarity_threshold', 0.85))

    def _proposal_items(proposal: list) -> list:
        return [p for p in proposal if isinstance(p, dict) and p.get('semantic')]

    def _dedupe_siblings_embed(items: list, threshold: float | None=None) -> list:
        threshold = threshold or _threshold()
        vectors = []
        result = []
        for p in items:
            vec = sentence_transformer_encode_util(p.get("semantic", ""))
            if not vec:
                result.append(p)
                continue
            if any((cosine_similarity_util(vec, v) > threshold for v in vectors)):
                continue
            vectors.append(vec)
            result.append(p)
        return result

    def _accept_light(parent_semantic: str, items: list) -> tuple:
        cfg = _growth_cfg()
        parent_max = float(cfg.get('parent_overlap_max', 0.92))
        sibling_max = float(cfg.get('sibling_overlap_max', 0.95))
        parent = str(parent_semantic or '').strip()
        pool = list(items)
        if parent:
            filtered = [p for p in pool if _jaccard(str(p.get('semantic', '')), parent) < parent_max]
            if filtered:
                pool = filtered
        accepted = []
        for p in pool:
            sem = str(p.get('semantic', ''))
            if any((_jaccard(sem, str(a.get('semantic', ''))) >= sibling_max for a in accepted)):
                continue
            accepted.append(p)
        if not accepted:
            accepted = pool[:max_children]
        if not accepted:
            accepted = items[:max_children]
        return (True, 'ok', accepted[:max_children])

    def _accept_off(items: list) -> tuple:
        seen = set()
        accepted = []
        for p in items:
            key = str(p.get('semantic', '')).strip().lower()
            if key in seen:
                continue
            seen.add(key)
            accepted.append(p)
        if not accepted:
            accepted = items[:max_children]
        return (True, 'ok', accepted[:max_children])

    def _accept_embedding(parent_semantic: str, items: list) -> tuple:
        if not parent_semantic:
            deduped = _dedupe_siblings_embed(items)
            return (True, 'ok', deduped if deduped else items[:max_children])
        threshold = _threshold()
        parent_vec = sentence_transformer_encode_util(str(parent_semantic))
        if not parent_vec:
            return (True, 'embed_unavailable', items[:max_children])
        scored = []
        for p in items:
            vec = sentence_transformer_encode_util(p.get("semantic", ""))
            if not vec:
                scored.append((p, 0.0))
                continue
            scored.append((p, cosine_similarity_util(vec, parent_vec)))
        if scored and all((sim > threshold for _, sim in scored)):
            return (False, 'all_steps_similar_to_parent', [])
        distinct = [p for p, sim in scored if sim <= threshold]
        if not distinct:
            return (False, 'no_distinct_steps', [])
        accepted = _dedupe_siblings_embed(distinct, threshold)
        if not accepted:
            return (False, 'siblings_collapsed', [])
        cfg = _growth_cfg()
        if not cfg.get('dedupe_siblings', True):
            accepted = distinct
        return (True, 'ok', accepted[:max_children])
    items = _proposal_items(proposal)
    if not items:
        return (False, 'empty_proposal', [])
    mode = _validation_mode()
    if mode == 'off':
        return _accept_off(items)
    if mode == 'light':
        return _accept_light(parent_semantic, items)
    return _accept_embedding(parent_semantic, items)
