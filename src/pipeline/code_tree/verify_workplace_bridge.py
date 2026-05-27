def verify_workplace_bridge(job_root: str, job_id: str | None = None) -> list[str]:
    """
    Adapter for verifying generated workplace contract from inside code_tree.
    """
    from pathlib import Path

    from src.verify_workplace_contract import verify_workplace_contract

    return verify_workplace_contract(Path(job_root), job_id=job_id)

