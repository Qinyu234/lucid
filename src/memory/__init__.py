import shutil
from datetime import datetime, timezone
from pathlib import Path

from src.log import get_logger, log_event
from src.schema.io import normalize_io

from .keywords import extract_keywords
from .retrieve import hybrid_retrieve
from .rerank import rerank_candidates
from .rules import check_io_compatible
from .store import load_entries, save_entries, shared_dir


def recall_for_reuse(node: dict, job_id: str | None = None) -> list:
    """
    1) keyword + embedding retrieve
    2) reranker rank
    3) static io rules filter (caller tries in order)
    """
    logger = get_logger(job_id)
    semantic = node.get("semantic", "")

    retrieved = hybrid_retrieve(semantic)
    if not retrieved:
        return []

    log_event(
        logger,
        "memory_retrieve",
        count=len(retrieved),
        top_module=retrieved[0].get("module"),
        top_score=retrieved[0].get("_retrieve_score"),
    )

    reranked = rerank_candidates(semantic, retrieved)
    if not reranked:
        return []

    log_event(
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
            log_event(
                logger,
                "memory_io_reject",
                level=30,
                module=cand.get("module"),
                reason=reason,
            )

    return passed


def render_reuse_wrapper(module: str) -> str:
    return (
        f"from shared.{module} import run as _shared_run\n\n\n"
        "def run(ctx):\n"
        "    return _shared_run(ctx)\n"
    )


def register_leaf(node: dict, code: str, file_path: str):

    module = node.get("function_name") or "unnamed"
    target = shared_dir() / f"{module}.py"

    if Path(file_path).exists():
        shutil.copy2(file_path, target)

    semantic = node.get("semantic", "")
    entries = load_entries()
    entries = [e for e in entries if e.get("module") != module]
    entries.append({
        "semantic": semantic,
        "keywords": extract_keywords(semantic),
        "module": module,
        "io": normalize_io(node.get("io")),
        "path": str(target),
        "updated": datetime.now(timezone.utc).isoformat(),
    })
    save_entries(entries)
    get_logger().info("memory registered module=%s", module)
