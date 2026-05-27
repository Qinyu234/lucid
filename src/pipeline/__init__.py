from .assess_job import assess_job
from .code_tree import code_tree
from .ensure_job_scaffold import ensure_job_scaffold
from .errors import errors
from .growth_loop import growth_loop
from .memory import memory
from .repair_node_code_path import repair_node_code_path
from .resolve_code_paths import resolve_code_paths
from .save_job_tree import save_job_tree
from .seed import seed
from .shared_ctx import shared_ctx


def pipeline(job):
    err = errors()
    PipelineError = err.PipelineError
    error_packet = err.error_packet
    ctx = shared_ctx({"data": {"job": job}, "meta": {}, "state": {}, "error": None})
    feature_util = ctx["meta"]["feature_util"]
    get_logger_util = ctx["meta"]["get_logger_util"]
    event_util = ctx["meta"]["event_util"]
    persist_registry_util = ctx["meta"]["persist_registry_util"]
    node_schema_util = ctx["meta"]["node_schema_util"]

    job_id = job.get("id", "unknown")
    logger = get_logger_util(job_id)
    root = None
    try:
        event_util(logger, "pipeline_start", job_id=job_id, goal=job.get("goal"))
        root = seed(job)
        ensure_job_scaffold(job)
        vr, root = node_schema_util(root)
        if not vr.ok:
            event_util(logger, "pipeline_seed_invalid", level=40, errors=vr.errors)
            save_job_tree(root, job, "seed_invalid", status="error", issues=vr.errors, job_id=job_id)
            return {"job_id": job_id, "status": "error", "errors": vr.errors, "tree": root}
        save_job_tree(root, job, "seed", status="growing", job_id=job_id)
        growth_loop(root, job_id=job_id, job=job)
        resolve_code_paths(root)
        save_job_tree(root, job, "growth_done", job_id=job_id)
        persist_registry_util(root, job)
        code_tree(root, job_id=job_id, job=job)
        save_job_tree(root, job, "code_done", job_id=job_id)
        persist_registry_util(root, job)
        status, issues = assess_job(root, job=job)
        save_job_tree(root, job, "pipeline_finish", status=status, issues=issues, job_id=job_id)
        event_util(logger, "pipeline_finish", status=status, issues=issues if issues else None)
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
