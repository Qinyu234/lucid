def resume_code_tree(job_id):
    import json
    from pathlib import Path

    from src.load_jobs import load_jobs
    from src.pipeline.assess_job import assess_job
    from src.pipeline.code_tree import code_tree
    from src.pipeline.resolve_code_paths import resolve_code_paths
    from src.pipeline.save_job_tree import save_job_tree
    from src.shared.get_logger import get_logger
    from src.shared.log_event import log_event
    from src.shared.persist_io_registry import persist_io_registry
    from src.shared.setup_logging import setup_logging

    setup_logging(job_id)
    logger = get_logger(job_id)
    data = load_jobs()
    job = next((j for j in data.get("jobs", []) if j.get("id") == job_id), None)
    if not job:
        raise SystemExit(f"unknown job_id: {job_id}")

    latest = Path(job["root_path"]) / "tree" / "latest.json"
    if not latest.is_file():
        raise SystemExit(f"missing tree snapshot: {latest}")

    payload = json.loads(latest.read_text(encoding="utf-8"))
    root = payload.get("tree")
    if not isinstance(root, dict):
        raise SystemExit("latest.json has no tree object")

    log_event(logger, "resume_code_tree_start", job_id=job_id, stage=payload.get("stage"))
    resolve_code_paths(root)
    save_job_tree(root, job, "growth_done", job_id=job_id)
    persist_io_registry(root, job)
    code_tree(root, job_id=job_id, job=job)
    save_job_tree(root, job, "code_done", job_id=job_id)
    persist_io_registry(root, job)
    status, issues = assess_job(root, job=job)
    save_job_tree(root, job, "pipeline_finish", status=status, issues=issues, job_id=job_id)
    log_event(logger, "resume_code_tree_finish", status=status, issues=issues or None)
    return {"job_id": job_id, "status": status, "issues": issues, "tree": root}
