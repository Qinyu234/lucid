def extract_keywords(text: str) -> list:
    from src.shared.lib.re_util import re_util
    if not text:
        return []
    lower = text.lower()
    re = re_util()
    words = re.findall(r"[a-z][a-z0-9_]{1,}", lower)
    words += re.findall(r"[\u4e00-\u9fff]{2,}", text)
    seen = set()
    result = []
    for w in words:
        if w not in seen:
            seen.add(w)
            result.append(w)
    return result
