from src.extract_json_object import extract_json_object
from src.llm import llm
from src.schema.io.empty_io import empty_io
from src.schema.io.normalize_io import normalize_io
from src.schema.validate_expand_output import validate_expand_output
from src.log.get_logger import get_logger

from .build_prompt import build_prompt

MAX_STEPS = 4


def expand(node, max_retry=3, job_id=None):

    def _normalize_step(raw):
        if isinstance(raw, str) and raw.strip():
            return {"semantic": raw.strip(), "tag": None, "io": empty_io()}

        if not isinstance(raw, dict):
            return None

        semantic = raw.get("semantic")
        if not semantic or not str(semantic).strip():
            return None

        tag = raw.get("tag")
        tag = None if tag in (None, "") else str(tag).strip()

        io = normalize_io(raw.get("io") or raw)

        return {
            "semantic": str(semantic).strip(),
            "tag": tag,
            "io": io,
        }

    logger = get_logger(job_id)

    for attempt in range(max_retry):

        raw = llm("expand", build_prompt(node), job_id=job_id)

        if not raw.strip():
            logger.warning("expand empty response attempt=%s", attempt)
            continue

        data = extract_json_object(raw)
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
        for item in raw_steps[:MAX_STEPS]:
            step = _normalize_step(item)
            if step:
                steps.append(step)

        if not steps:
            continue

        payload = {
            "steps": steps,
            "io": normalize_io(data.get("io")),
        }

        vr = validate_expand_output(payload)
        if not vr.ok:
            logger.warning("expand schema invalid attempt=%s errors=%s", attempt, vr.errors)
            if steps:
                return payload
            continue

        return payload

    logger.error("expand exhausted retries node=%s", node.get("semantic"))
    return {"steps": [], "io": empty_io()}
