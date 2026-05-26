def llm(scenario: str, prompt: str, job_id: str | None=None) -> str:
    import requests

    from src.shared.feature_enabled import feature_enabled
    from src.shared.get_llm_scenario import get_llm_scenario
    from src.shared.get_logger import get_logger

    def _build_payload(profile: dict, prompt: str, use_format: bool) -> dict:
        payload = {'model': profile['model'], 'prompt': prompt, 'stream': False}
        fmt = profile.get('format')
        if use_format and fmt:
            payload['format'] = fmt
        if feature_enabled('ollama_unload_after_request'):
            payload['keep_alive'] = 0
        return payload

    def _extract_response(data: dict) -> str:
        if not isinstance(data, dict):
            return ''
        text = data.get('response') or data.get('message', {}).get('content', '')
        if isinstance(text, dict):
            text = text.get('content', '')
        return (text or '').strip()
    profile = get_llm_scenario(scenario)
    logger = get_logger(job_id)
    url = profile['api_url']
    timeout = int(profile.get('timeout_sec', 120))
    tries = [True, False] if profile.get('format') else [False]
    last_err = None
    for use_format in tries:
        payload = _build_payload(profile, prompt, use_format)
        try:
            response = requests.post(url, json=payload, timeout=timeout)
            if not response.ok:
                body = (response.text or '')[:500]
                logger.error('llm http error scenario=%s status=%s format=%s body=%s', scenario, response.status_code, use_format, body)
                if use_format and response.status_code >= 500:
                    last_err = f'HTTP {response.status_code}'
                    continue
                return ''
            data = response.json()
            text = _extract_response(data)
            if not text:
                logger.warning('llm empty response scenario=%s format=%s', scenario, use_format)
                if use_format:
                    continue
                return ''
            if use_format and profile.get('format'):
                logger.debug('llm ok scenario=%s with format=%s', scenario, profile.get('format'))
            elif profile.get('format'):
                logger.info('llm ok scenario=%s without format (fallback)', scenario)
            return text
        except requests.RequestException as e:
            last_err = str(e)
            logger.error('llm request failed scenario=%s format=%s err=%s', scenario, use_format, e)
            if use_format:
                continue
            return ''
    if last_err:
        logger.error('llm all attempts failed scenario=%s last=%s', scenario, last_err)
    return ''
