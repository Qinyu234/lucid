def embed_model(text: str):
    from sentence_transformers import SentenceTransformer

    def _get_model():
        global _model
        if _model is None:
            _model = SentenceTransformer('all-MiniLM-L6-v2')
        return _model
    if not isinstance(text, str):
        text = str(text)
    if text in _cache:
        return _cache[text]
    vec = _get_model().encode(text)
    if len(_cache) >= 512:
        _cache.clear()
    _cache[text] = vec
    return vec
