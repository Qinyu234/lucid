def save_job_tree(
    root: dict,
    job: dict,
    stage: str,
    *,
    status: str | None = None,
    issues: list | None = None,
    extra: dict | None = None,
    job_id: str | None = None,
):
    from src.shared.lib.save_job_tree_util import save_job_tree_util

    return save_job_tree_util(
        root, job, stage, status=status, issues=issues, extra=extra, job_id=job_id
    )
