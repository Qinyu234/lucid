def hybrid_retrieve(query_semantic: str, top_k: int | None = None) -> list:
    from src.shared.lib.hybrid_retrieve_util import hybrid_retrieve_util

    return hybrid_retrieve_util(query_semantic, top_k)
