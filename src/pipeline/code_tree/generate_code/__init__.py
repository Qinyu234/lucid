from .build_prompt import build_prompt
from .invoke_llm import invoke_llm
from .leaf_stub import leaf_stub
from .recall_code import recall_code
from .render_reuse import render_reuse
from .shared_ctx import shared_ctx
from .stub_policy import stub_policy
from .verify_code import verify_code
from .verify_shared_code import verify_shared_code


def generate_code(node, max_retry=None, job_id=None, root=None):
    ctx = shared_ctx({"data": {}, "meta": {}, "state": {}, "error": None})
    get_logger_util = ctx["meta"]["get_logger_util"]
    app_config_util = ctx["meta"]["app_config_util"]
    event_util = ctx["meta"]["event_util"]

    logger = get_logger_util(job_id)
    fn = node.get("function_name") or "module"
    semantic = str(node.get("semantic", "") or "")
    cfg = app_config_util().get("codegen", {})
    stub_on_fail = cfg.get("stub_on_fail", True)
    if stub_policy(semantic, cfg):
        stub = leaf_stub(node)
        ok, err = verify_code(stub, node)
        if ok:
            node["code_kind"] = "stub_policy"
            event_util(
                logger,
                "code_gen_stub_policy",
                level=30,
                function_name=fn,
                semantic=semantic[:200],
            )
            return stub
        event_util(logger, "code_gen_stub_policy_invalid", level=40, error=err, function_name=fn)
    if max_retry is None:
        max_retry = int(cfg.get("max_retry", 6))
    for cand in recall_code(node, job_id=job_id):
        code = render_reuse(node, cand["module"])
        ok, err = verify_code(code, node)
        if ok:
            node["code_kind"] = "reuse"
            event_util(
                logger,
                "memory_reuse_ok",
                module=cand.get("module"),
                rerank=cand.get("_rerank_score"),
            )
            return code
        event_util(
            logger,
            "memory_reuse_verify_fail",
            level=30,
            module=cand.get("module"),
            error=err,
        )
    for attempt in range(max_retry):
        code = invoke_llm("code", build_prompt(node, root=root), job_id=job_id)
        ok, err = verify_code(code, node)
        if ok:
            node["code_kind"] = "llm"
            return code
        event_util(
            logger,
            "code_gen_verify_fail",
            level=30,
            attempt=attempt,
            error=err,
            function_name=fn,
        )
    if stub_on_fail:
        stub = leaf_stub(node)
        ok, err = verify_code(stub, node)
        if ok:
            node["code_kind"] = "stub"
            event_util(
                logger,
                "code_gen_stub_fallback",
                level=30,
                function_name=fn,
                semantic=node.get("semantic"),
            )
            return stub
        event_util(logger, "code_gen_stub_invalid", level=40, error=err)
    event_util(logger, "code_gen_exhausted", level=40, semantic=node.get("semantic"))
    return ""
