def recall_for_reuse(node: dict, job_id: str | None = None) -> list:
    from src.shared.lib.recall_for_reuse_util import recall_for_reuse_util

    return recall_for_reuse_util(node, job_id)
