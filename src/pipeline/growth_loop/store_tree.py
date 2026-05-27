def store_tree(
    root: dict,
    job: dict | None,
    stage: str,
    *,
    status: str | None = None,
    issues: list | None = None,
    extra: dict | None = None,
    job_id: str | None = None,
):
    from src.shared.lib.store_tree_util import store_tree_util

    return store_tree_util(
        root, job, stage, status=status, issues=issues, extra=extra, job_id=job_id
    )
