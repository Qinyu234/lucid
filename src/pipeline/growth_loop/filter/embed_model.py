from sentence_transformers import SentenceTransformer

_model = None
_cache: dict[str, object] = {}


def embed_model(text: str):

    def _get_model():
        global _model
        if _model is None:
            _model = SentenceTransformer("all-MiniLM-L6-v2")
        return _model

    if not isinstance(text, str):
        text = str(text)

    if text in _cache:
        return _cache[text]

    vec = _get_model().encode(text)
    _cache[text] = vec
    return vec
