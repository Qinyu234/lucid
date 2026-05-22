import logging

from src.errors import PipelineError, error_packet
from src.log import get_logger, log_event
from src.schema import validate_node

from .seed import seed
from .growth_loop import growth_loop
from .code_tree import code_tree
from .is_fully_grown import is_fully_grown


def pipeline(job):

    job_id = job.get("id", "unknown")
    logger = get_logger(job_id)

    try:
        log_event(logger, "pipeline_start", job_id=job_id, goal=job.get("goal"))

        root = seed(job)

        vr, root = validate_node(root)
        if not vr.ok:
            log_event(logger, "pipeline_seed_invalid", level=logging.ERROR, errors=vr.errors)
            return {
                "job_id": job_id,
                "status": "error",
                "errors": vr.errors,
                "tree": root,
            }

        growth_loop(root, job_id=job_id)
        code_tree(root, job_id=job_id)

        status = "done" if is_fully_grown(root) else "incomplete"

        log_event(logger, "pipeline_finish", status=status)

        return {
            "job_id": job_id,
            "status": status,
            "tree": root,
        }

    except PipelineError as e:
        logger.error("%s: %s", e.code, e.message)
        packet = e.to_packet()
        packet["job_id"] = job_id
        packet["status"] = "error"
        return packet

    except Exception as e:
        logger.exception("pipeline_unhandled")
        packet = error_packet("PIPELINE_ERROR", str(e))
        packet["job_id"] = job_id
        packet["status"] = "error"
        return packet
