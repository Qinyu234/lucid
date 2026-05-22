from .log import get_logger, log_event


def report(job: dict, result: dict) -> dict:

    logger = get_logger(job.get("id"))
    job_id = job.get("id", "unknown")
    status = result.get("status", "unknown")

    summary = {
        "job_id": job_id,
        "status": status,
        "issues": result.get("issues"),
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
    log_event(logger, "job_report", level=level, **{k: v for k, v in summary.items() if v is not None})

    return summary
