def keyword_score(query_kw: list, entry_kw: list) -> float:
    if not query_kw or not entry_kw:
        return 0.0

    qs = set(query_kw)
    es = set(entry_kw)
    overlap = len(qs & es)
    if overlap == 0:
        return 0.0

    return overlap / len(qs)
