import logging

from src.errors import PipelineError, error_packet
from src.log.get_logger import get_logger
from src.log.log_event import log_event
from src.schema.persist_io_registry import persist_io_registry
from src.schema.validate_node import validate_node

from .assess_job import assess_job
from .seed import seed
from .growth_loop import growth_loop
from .code_tree import code_tree
from .resolve_code_paths import resolve_code_paths
from .save_job_tree import save_job_tree


def pipeline(job):

    job_id = job.get("id", "unknown")
    logger = get_logger(job_id)
    root = None

    try:
        log_event(logger, "pipeline_start", job_id=job_id, goal=job.get("goal"))

        from src.algorithm.ensure_layout import ensure_layout
        ensure_layout()

        root = seed(job)

        vr, root = validate_node(root)
        if not vr.ok:
            log_event(logger, "pipeline_seed_invalid", level=logging.ERROR, errors=vr.errors)
            save_job_tree(root, job, "seed_invalid", status="error", issues=vr.errors, job_id=job_id)
            return {
                "job_id": job_id,
                "status": "error",
                "errors": vr.errors,
                "tree": root,
            }

        save_job_tree(root, job, "seed", status="growing", job_id=job_id)

        growth_loop(root, job_id=job_id, job=job)

        resolve_code_paths(root)

        save_job_tree(root, job, "growth_done", job_id=job_id)

        persist_io_registry(root, job)

        code_tree(root, job_id=job_id, job=job)

        save_job_tree(root, job, "code_done", job_id=job_id)
        persist_io_registry(root, job)

        status, issues = assess_job(root)

        save_job_tree(root, job, "pipeline_finish", status=status, issues=issues, job_id=job_id)

        log_event(
            logger,
            "pipeline_finish",
            status=status,
            issues=issues if issues else None,
        )

        return {
            "job_id": job_id,
            "status": status,
            "issues": issues,
            "tree": root,
            "tree_path": str(job.get("root_path", "")) + "/tree/latest.json",
        }

    except PipelineError as e:
        logger.error("%s: %s", e.code, e.message)
        if root is not None:
            save_job_tree(root, job, "error", status="error", issues=[e.message], job_id=job_id)
        packet = e.to_packet()
        packet["job_id"] = job_id
        packet["status"] = "error"
        if root is not None:
            packet["tree"] = root
        return packet

    except Exception as e:
        logger.exception("pipeline_unhandled")
        if root is not None:
            save_job_tree(root, job, "error", status="error", issues=[str(e)], job_id=job_id)
        packet = error_packet("PIPELINE_ERROR", str(e))
        packet["job_id"] = job_id
        packet["status"] = "error"
        if root is not None:
            packet["tree"] = root
        return packet
