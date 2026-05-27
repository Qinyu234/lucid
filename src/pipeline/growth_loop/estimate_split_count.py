def estimate_split_count(semantic: str, cfg: dict | None = None, depth: int = 0) -> int:
    """
    Heuristic target step count before expand (no extra LLM call).

    Signals: conjunctions / list markers, numbered clauses, text length.
    Result clamped to growth.min_children .. growth.max_children (default 2..6).
    """
    from src.shared.lib.re_util import re_util

    growth = cfg or {}
    min_n = int(growth.get("min_children", 2))
    max_n = int(growth.get("max_children", 6))
    if depth <= 0:
        max_n = min(max_n, int(growth.get("max_children_root", 3)))
    if min_n > max_n:
        min_n, max_n = max_n, min_n
    text = (semantic or "").strip()
    if not text:
        return min_n
    re = re_util()
    score = min_n
    separators = len(
        re.findall(
            r"[、,，;；]|以及|并且|然后|其次|最后|同时|另外|first|then|finally|also|and\b",
            text,
            re.I,
        )
    )
    if separators:
        score = max(score, min(min_n + separators, max_n))
    numbered = len(re.findall(r"(\d+[\.\)、]|[（(]\d+[)）]|第[一二三四五六七八])", text))
    if numbered >= 2:
        score = max(score, min(numbered, max_n))
    if len(text) > 80:
        score = max(score, 3)
    if len(text) > 160:
        score = max(score, 4)
    if len(text) > 240:
        score = max(score, 5)
    return max(min_n, min(max_n, score))
