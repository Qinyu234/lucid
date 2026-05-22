import logging

from src.llm import call_llm
from src.log import get_logger, log_event
from src.memory import ask_reuse, find_similar, register_leaf, render_reuse_wrapper

from .build_prompt import build_prompt
from .verify_code import verify_code


def generate_code(node, max_retry=3, job_id=None):

    logger = get_logger(job_id)

    similar = find_similar(node.get("semantic", ""))
    if similar:
        decision = ask_reuse(node, similar, job_id=job_id)
        log_event(
            logger,
            "memory_reuse_check",
            reuse=decision.get("reuse"),
            reason=decision.get("reason"),
            module=similar.get("module"),
        )
        if decision.get("reuse"):
            code = render_reuse_wrapper(similar["module"])
            ok, err = verify_code(code, node)
            if ok:
                return code
            log_event(logger, "memory_reuse_verify_fail", level=logging.WARNING, error=err)

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
