def rerank_candidates(query_semantic: str, candidates: list) -> list:
    from src.shared.lib.rerank_candidates_util import rerank_candidates_util

    return rerank_candidates_util(query_semantic, candidates)
