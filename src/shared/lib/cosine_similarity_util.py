def cosine_similarity_util(a: list | None, b: list | None) -> float:
    if not a or not b:
        return 0.0
    if len(a) != len(b):
        return 0.0
    dot = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b):
        try:
            fx = float(x)
            fy = float(y)
        except Exception:
            return 0.0
        dot += fx * fy
        na += fx * fx
        nb += fy * fy
    denom = (na ** 0.5) * (nb ** 0.5)
    if denom == 0.0:
        return 0.0
    return float(dot / denom)

