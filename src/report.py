def report(job: dict, result: dict) -> dict:
    from src.shared.logging.get_logger_util import get_logger_util
    from src.shared.logging.event_util import event_util

    logger = get_logger_util(job.get("id"))
    job_id = job.get("id", "unknown")
    status = result.get("status", "unknown")

    summary = {
        "job_id": job_id,
        "status": status,
        "issues": result.get("issues"),
        "tree_path": result.get("tree_path"),
        "errors": result.get("errors"),
        "code": result.get("code"),
        "message": result.get("message"),
    }

    if status == "error":
        level = 40
    elif status == "incomplete":
        level = 30
    else:
        level = 20
    event_util(logger, "job_report", level=level, **{k: v for k, v in summary.items() if v is not None})

    return summary
