import requests

from .config import get_llm_scenario
from .log import get_logger


def call_llm(scenario: str, prompt: str, job_id: str | None = None) -> str:

    profile = get_llm_scenario(scenario)
    logger = get_logger(job_id)

    payload = {
        "model": profile["model"],
        "prompt": prompt,
        "stream": False,
    }

    fmt = profile.get("format")
    if fmt:
        payload["format"] = fmt

    try:
        response = requests.post(
            profile["api_url"],
            json=payload,
            timeout=int(profile.get("timeout_sec", 120)),
        )
        response.raise_for_status()
        data = response.json()
        text = data.get("response", "") or ""
        if not text.strip():
            logger.warning("llm empty response scenario=%s", scenario)
        return text

    except Exception as e:
        logger.error("llm call failed scenario=%s err=%s", scenario, e)
        return ""
