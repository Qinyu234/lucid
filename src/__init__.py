from .finish import finish
from .format_runtime_error import format_runtime_error
from .load_jobs import load_jobs
from .pipeline import pipeline
from .report import report
from .resume_code_tree import resume_code_tree
from .runtime_logging import runtime_logging
from .run_one_job import run_one_job
from .shared import shared
from .validator import validator


def src():
    import logging

    ctx = runtime_logging({"data": {}, "meta": {}, "state": {}, "error": None})
    logger = ctx["meta"]["logger"]
    event_util = ctx["meta"]["event_util"]

    try:
        event_util(logger, "runtime_start")
        data = load_jobs()
        event_util(logger, "io_loaded", job_count=len(data.get("jobs", [])))
        valid_packet = validator(data)
        if not valid_packet.get("valid", False):
            event_util(
                logger,
                "validation_failed",
                level=logging.ERROR,
                message=valid_packet.get("message"),
            )
            return valid_packet
        jobs = valid_packet["data"]["jobs"]
        results = []
        event_util(logger, "jobs_start", count=len(jobs))
        for i, job in enumerate(jobs):
            event_util(logger, "job_start", index=i, job_id=job.get("id"))
            result = pipeline(job)
            report_out = report(job, result)
            results.append({"job": job, "result": result, "report": report_out})
            if result.get("status") == "error":
                event_util(
                    logger,
                    "job_error",
                    level=logging.ERROR,
                    job_id=job.get("id"),
                    code=result.get("code"),
                    message=result.get("message"),
                )
        final = finish({"results": results})
        event_util(logger, "runtime_finish", status=final.get("status"))
        return final
    except Exception as exc:
        logger.exception("runtime_unhandled")
        return format_runtime_error(exc)
