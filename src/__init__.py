import logging

from .io import io
from .validator import validator
from .report import report
from .finish import finish
from .log import setup_logging, get_logger, log_event
from .errors import error_packet


def src():

    from .pipeline import pipeline

    setup_logging()
    logger = get_logger()

    try:
        log_event(logger, "runtime_start")

        data = io()
        log_event(logger, "io_loaded", job_count=len(data.get("jobs", [])))

        valid_packet = validator(data)

        if not valid_packet.get("valid", False):
            log_event(
                logger,
                "validation_failed",
                level=logging.ERROR,
                message=valid_packet.get("message"),
            )
            return valid_packet

        jobs = valid_packet["data"]["jobs"]
        results = []

        log_event(logger, "jobs_start", count=len(jobs))

        for i, job in enumerate(jobs):

            log_event(logger, "job_start", index=i, job_id=job.get("id"))

            result = pipeline(job)

            report_out = report(job, result)

            results.append({
                "job": job,
                "result": result,
                "report": report_out,
            })

            if result.get("status") == "error":
                log_event(
                    logger,
                    "job_error",
                    level=logging.ERROR,
                    job_id=job.get("id"),
                    code=result.get("code"),
                    message=result.get("message"),
                )

        final = finish({"results": results})

        log_event(logger, "runtime_finish", status=final.get("status"))

        return final

    except Exception as e:
        logger.exception("runtime_unhandled")
        return error_packet("RUNTIME_ERROR", str(e))
