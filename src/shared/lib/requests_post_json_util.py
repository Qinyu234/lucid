def requests_post_json_util(url: str, payload: dict, timeout_sec: int) -> dict:
    """
    Thin wrapper around requests.post(..., json=payload, timeout=...).
    Returns a dict with keys: ok(bool), status_code(int|None), text(str), json(dict|list|None), error(str|None)
    """

    try:
        import requests  # third-party; imported inside function
    except Exception as e:
        return {"ok": False, "status_code": None, "text": "", "json": None, "error": f"requests_unavailable: {e}"}

    try:
        resp = requests.post(url, json=payload, timeout=int(timeout_sec))
        data = None
        try:
            data = resp.json()
        except Exception:
            data = None
        return {
            "ok": bool(getattr(resp, "ok", False)),
            "status_code": getattr(resp, "status_code", None),
            "text": (getattr(resp, "text", "") or ""),
            "json": data,
            "error": None,
        }
    except Exception as e:
        return {"ok": False, "status_code": None, "text": "", "json": None, "error": str(e)}

