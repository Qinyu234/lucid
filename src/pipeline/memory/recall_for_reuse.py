def recall_for_reuse(node: dict, job_id: str | None = None) -> list:
    from src.pipeline.memory.check_io_compatible import check_io_compatible
    from src.pipeline.memory.hybrid_retrieve import hybrid_retrieve
    from src.pipeline.memory.rerank_candidates import rerank_candidates
    from src.shared.lib.feature_util import feature_util
    from src.shared.logging.event_util import event_util
    from src.shared.logging.get_logger_util import get_logger_util

    logger = get_logger_util(job_id)
    semantic = node.get("semantic", "")
    if not feature_util("memory_recall"):
        return []
    retrieved = hybrid_retrieve(semantic)
    if not retrieved:
        return []
    event_util(
        logger,
        "memory_retrieve",
        count=len(retrieved),
        top_module=retrieved[0].get("module"),
        top_score=retrieved[0].get("_retrieve_score"),
    )
    reranked = rerank_candidates(semantic, retrieved)
    if not reranked:
        return []
    event_util(
        logger,
        "memory_rerank",
        count=len(reranked),
        top_module=reranked[0].get("module"),
        top_rerank=reranked[0].get("_rerank_score"),
    )
    passed = []
    for cand in reranked:
        ok, reason = check_io_compatible(node, cand)
        if ok:
            cand["_io_rule"] = "pass"
            passed.append(cand)
        else:
            event_util(
                logger,
                "memory_io_reject",
                level=30,
                module=cand.get("module"),
                reason=reason,
            )
    return passed
