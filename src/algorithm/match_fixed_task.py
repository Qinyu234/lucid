import re

from src.algorithm.list_algorithms import list_algorithms


def match_fixed_task(node: dict, limit: int = 6) -> list:
    """
    Rank algorithms whose fixed_task.business/distribution overlap node semantic/io.
    Only returns entries with explicit fixed_task + relative_advantage.
    """

    def tokens(text: str) -> set:
        if not text:
            return set()
        return set(re.findall(r"[a-zA-Z0-9_]{3,}", text.lower()))

    semantic = node.get("semantic", "") or ""
    io = node.get("io") or {}
    io_keys = []
    for side in ("in", "out"):
        for field in io.get(side, []):
            if isinstance(field, dict):
                io_keys.append(field.get("name", ""))
            elif isinstance(field, str):
                io_keys.append(field)

    query_tokens = tokens(semantic) | tokens(" ".join(io_keys))
    if not query_tokens:
        return list_algorithms(limit=limit)

    scored = []
    for entry in list_algorithms(limit=100):
        fixed = entry.get("fixed_task") or {}
        adv = entry.get("relative_advantage") or {}
        if not fixed.get("profile_id") or not adv.get("baseline"):
            continue

        hay = " ".join([
            fixed.get("distribution", ""),
            fixed.get("business", ""),
            " ".join(fixed.get("constraints") or []),
            entry.get("semantic", ""),
            entry.get("category", ""),
        ])
        hay_tokens = tokens(hay)
        if not hay_tokens:
            continue

        overlap = len(query_tokens & hay_tokens)
        if overlap <= 0:
            continue

        scored.append((overlap, entry))

    scored.sort(key=lambda x: (-x[0], x[1].get("function_name", "")))
    return [entry for _, entry in scored[:limit]]
