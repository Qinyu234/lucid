import re


def extract_keywords(text: str) -> list:
    if not text:
        return []

    lower = text.lower()
    words = re.findall(r"[a-z][a-z0-9_]{1,}", lower)
    words += re.findall(r"[\u4e00-\u9fff]{2,}", text)

    seen = set()
    result = []
    for w in words:
        if w not in seen:
            seen.add(w)
            result.append(w)
    return result
