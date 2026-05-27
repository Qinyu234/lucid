def llm_util(scenario: str, prompt: str, job_id: str | None = None) -> str:
    from src.shared.lib.feature_util import feature_util
    from src.shared.lib.llm_scenario_util import llm_scenario_util
    from src.shared.lib.requests_post_json_util import requests_post_json_util
    from src.shared.logging.get_logger_util import get_logger_util

    def _build_payload(profile: dict, prompt: str, use_format: bool) -> dict:
        payload = {"model": profile["model"], "prompt": prompt, "stream": False}
        fmt = profile.get("format")
        if use_format and fmt:
            payload["format"] = fmt
        if feature_util("ollama_unload_after_request"):
            payload["keep_alive"] = 0
        return payload

    def _extract_response(data: dict) -> str:
        if not isinstance(data, dict):
            return ""
        text = data.get("response") or data.get("message", {}).get("content", "")
        if isinstance(text, dict):
            text = text.get("content", "")
        return (text or "").strip()

    profile = llm_scenario_util(scenario)
    logger = get_logger_util(job_id)
    url = profile["api_url"]
    timeout = int(profile.get("timeout_sec", 120))
    tries = [True, False] if profile.get("format") else [False]
    last_err = None
    for use_format in tries:
        payload = _build_payload(profile, prompt, use_format)
        res = requests_post_json_util(url, payload, timeout)
        if not res.get("ok"):
            status = res.get("status_code")
            body = (res.get("text") or "")[:500]
            err = res.get("error") or ""
            logger.error(
                "llm http error scenario=%s status=%s format=%s body=%s err=%s",
                scenario,
                status,
                use_format,
                body,
                err,
            )
            if use_format and (isinstance(status, int) and status >= 500):
                last_err = f"HTTP {status}"
                continue
            last_err = err or (f"HTTP {status}" if status is not None else "request_failed")
            if use_format:
                continue
            return ""

        data = res.get("json")
        text = _extract_response(data if isinstance(data, dict) else {})
        if not text:
            logger.warning("llm empty response scenario=%s format=%s", scenario, use_format)
            if use_format:
                continue
            return ""
        if use_format and profile.get("format"):
            logger.debug("llm ok scenario=%s with format=%s", scenario, profile.get("format"))
        elif profile.get("format"):
            logger.info("llm ok scenario=%s without format (fallback)", scenario)
        return text
    if last_err:
        logger.error("llm all attempts failed scenario=%s last=%s", scenario, last_err)
    return ""
