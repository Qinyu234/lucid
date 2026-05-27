def sentence_transformer_encode_util(text: str) -> list | None:
    """
    Encode text into a vector using SentenceTransformer.
    Returns a Python list (or None if unavailable).
    """
    try:
        from sentence_transformers import SentenceTransformer  # third-party; imported inside function
    except Exception:
        return None

    if not isinstance(text, str):
        text = str(text)
    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        vec = model.encode(text)
        try:
            return vec.tolist()  # numpy array -> list
        except Exception:
            return list(vec)
    except Exception:
        return None

