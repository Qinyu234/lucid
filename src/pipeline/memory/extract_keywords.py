def extract_keywords(text: str) -> list:
    import re
    if not text:
        return []
    lower = text.lower()
    words = re.findall('[a-z][a-z0-9_]{1,}', lower)
    words += re.findall('[\\u4e00-\\u9fff]{2,}', text)
    seen = set()
    result = []
    for w in words:
        if w not in seen:
            seen.add(w)
            result.append(w)
    return result
