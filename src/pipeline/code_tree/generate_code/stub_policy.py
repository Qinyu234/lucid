def stub_policy(semantic: str, cfg: dict) -> bool:
    """
    Decide whether to force deterministic stub for a leaf.
    """
    from src.shared.lib.re_util import re_util

    if not semantic:
        return False
    if not bool(cfg.get("force_stub_on_patterns", True)):
        return False
    patterns = cfg.get("stub_patterns") or []
    re = re_util()
    for pat in patterns:
        if not isinstance(pat, str) or not pat:
            continue
        if re.search(pat, semantic, re.I):
            return True
    return False

