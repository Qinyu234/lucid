def resume_code_tree(job_id):
    from src.load_jobs import load_jobs
    from src.pipeline import assess_job, code_tree, resolve_code_paths, save_job_tree
    from src.shared.io_tree.persist_registry_util import persist_registry_util
    from src.shared.lib.json_read_file_util import json_read_file_util
    from src.shared.lib.path_is_file_util import path_is_file_util
    from src.shared.logging.event_util import event_util
    from src.shared.logging.get_logger_util import get_logger_util
    from src.shared.logging.setup_util import setup_util

    setup_util(job_id)
    logger = get_logger_util(job_id)
    data = load_jobs()
    job = next((j for j in data.get("jobs", []) if j.get("id") == job_id), None)
    if not job:
        raise SystemExit(f"unknown job_id: {job_id}")

    latest = str(job["root_path"]).rstrip("/").rstrip("\\") + "/tree/latest.json"
    if not path_is_file_util(latest):
        raise SystemExit(f"missing tree snapshot: {latest}")

    payload = json_read_file_util(latest, default={})
    root = payload.get("tree")
    if not isinstance(root, dict):
        raise SystemExit("latest.json has no tree object")

    event_util(logger, "resume_code_tree_start", job_id=job_id, stage=payload.get("stage"))
    resolve_code_paths(root)
    save_job_tree(root, job, "growth_done", job_id=job_id)
    persist_registry_util(root, job)
    code_tree(root, job_id=job_id, job=job)
    save_job_tree(root, job, "code_done", job_id=job_id)
    persist_registry_util(root, job)
    status, issues = assess_job(root, job=job)
    save_job_tree(root, job, "pipeline_finish", status=status, issues=issues, job_id=job_id)
    event_util(logger, "resume_code_tree_finish", status=status, issues=issues or None)
    return {"job_id": job_id, "status": status, "issues": issues, "tree": root}
