from .build_prompt import build_prompt
from .extract_json import extract_json
from .invoke_llm import invoke_llm
from .shared_ctx import shared_ctx


def expand(node, max_retry=None, job_id=None):
    import time

    max_steps = 4
    ctx = shared_ctx({"data": {}, "meta": {}, "state": {}, "error": None})
    io_empty_util = ctx["meta"]["io_empty_util"]
    get_logger_util = ctx["meta"]["get_logger_util"]
    app_config_util = ctx["meta"]["app_config_util"]
    io_normalize_util = ctx["meta"]["io_normalize_util"]
    expand_output_util = ctx["meta"]["expand_output_util"]

    def _normalize_step(raw):
        if isinstance(raw, str) and raw.strip():
            return {"semantic": raw.strip(), "tag": None, "io": io_empty_util()}
        if not isinstance(raw, dict):
            return None
        semantic = raw.get("semantic")
        if not semantic or not str(semantic).strip():
            return None
        tag = raw.get("tag")
        tag = None if tag in (None, "") else str(tag).strip()
        io = io_normalize_util(raw.get("io") or raw)
        return {"semantic": str(semantic).strip(), "tag": tag, "io": io}

    if max_retry is None:
        max_retry = int(app_config_util().get("growth", {}).get("max_expand_retry", 6))
    logger = get_logger_util(job_id)
    for attempt in range(max_retry):
        raw = invoke_llm("expand", build_prompt(node), job_id=job_id)
        if not raw.strip():
            logger.warning("expand empty response attempt=%s", attempt)
            if attempt + 1 < max_retry:
                time.sleep(min(30, 5 * (attempt + 1)))
            continue
        data = extract_json(raw)
        if data is None:
            logger.warning(
                "expand json parse failed attempt=%s preview=%s",
                attempt,
                raw[:200].replace("\n", " "),
            )
            continue
        raw_steps = data.get("steps")
        if not isinstance(raw_steps, list) or len(raw_steps) == 0:
            continue
        steps = []
        for item in raw_steps[:max_steps]:
            step = _normalize_step(item)
            if step:
                steps.append(step)
        if not steps:
            continue
        payload = {"steps": steps, "io": io_normalize_util(data.get("io"))}
        vr = expand_output_util(payload)
        if not vr.ok:
            logger.warning("expand schema invalid attempt=%s errors=%s", attempt, vr.errors)
            continue
        return payload
    logger.error("expand exhausted retries node=%s", node.get("semantic"))
    return {"steps": [], "io": io_empty_util()}
