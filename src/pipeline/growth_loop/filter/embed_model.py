# =========================
# FUNCTION:
# embed
#
# PURPOSE:
# convert text to vector using sentence-transformers
# =========================


from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_model(text: str):

    if not isinstance(text, str):
        text = str(text)

    return _model.encode(text)