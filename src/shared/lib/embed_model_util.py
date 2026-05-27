def embed_model_util(text: str):
    from src.shared.lib.sentence_transformer_encode_util import sentence_transformer_encode_util

    if not hasattr(embed_model_util, "_cache"):
        embed_model_util._cache = {}
    cache = embed_model_util._cache
    if not isinstance(text, str):
        text = str(text)
    if text in cache:
        return cache[text]
    vec = sentence_transformer_encode_util(text)
    if vec is None:
        return None
    if len(cache) >= 512:
        cache.clear()
    cache[text] = vec
    return vec
