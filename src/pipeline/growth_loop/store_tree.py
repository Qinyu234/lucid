from pathlib import Path
from typing import Optional

from src.pipeline.save_job_tree import save_job_tree as _save_job_tree


def store_tree(
    root: dict,
    job: Optional[dict],
    stage: str,
    *,
    status: Optional[str] = None,
    issues: Optional[list] = None,
    extra: Optional[dict] = None,
    job_id: Optional[str] = None,
) -> Optional[Path]:
    """Persist growth tree snapshot under job workspace: {root_path}/tree/latest.json."""
    if job is None:
        return None

    return _save_job_tree(
        root,
        job,
        stage,
        status=status,
        issues=issues,
        extra=extra,
        job_id=job_id,
    )
