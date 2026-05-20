from sentence_transformers import SentenceTransformer

# 建议全局只加载一次（避免重复初始化）
_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def embed(text: str):
    """
    将文本转换为 embedding 向量
    """
    vec = _model.encode(text, normalize_embeddings=True)
    return vec