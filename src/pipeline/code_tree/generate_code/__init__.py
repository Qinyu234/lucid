import logging

from src.llm import call_llm
from src.log import get_logger, log_event
from src.memory import recall_for_reuse, render_reuse_wrapper

from .build_prompt import build_prompt
from .verify_code import verify_code


def generate_code(node, max_retry=3, job_id=None):

    logger = get_logger(job_id)

    for cand in recall_for_reuse(node, job_id=job_id):
        code = render_reuse_wrapper(cand["module"])
        ok, err = verify_code(code, node)
        if ok:
            log_event(
                logger,
                "memory_reuse_ok",
                module=cand.get("module"),
                rerank=cand.get("_rerank_score"),
                retrieve=cand.get("_retrieve_score"),
            )
            return code
        log_event(
            logger,
            "memory_reuse_verify_fail",
            level=logging.WARNING,
            module=cand.get("module"),
            error=err,
        )

    for attempt in range(max_retry):

        code = call_llm("code", build_prompt(node), job_id=job_id)

        ok, err = verify_code(code, node)
        if ok:
            return code

        log_event(
            logger,
            "code_gen_verify_fail",
            level=logging.WARNING,
            attempt=attempt,
            error=err,
            function_name=node.get("function_name"),
        )

    log_event(
        logger,
        "code_gen_exhausted",
        level=logging.ERROR,
        semantic=node.get("semantic"),
    )
    return ""
