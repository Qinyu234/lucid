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
    """Persist growth tree snapshot under job workspace: {root_path}/tree/latest.json."""
    from src.pipeline.save_job_tree import save_job_tree as _save_job_tree

    if job is None:
        return None
    return _save_job_tree(
        root, job, stage, status=status, issues=issues, extra=extra, job_id=job_id
    )
