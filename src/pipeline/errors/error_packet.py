def error_packet(code: str, message: str, detail: dict | None = None) -> dict:
    return {
        "ok": False,
        "code": code,
        "message": message,
        "detail": detail or {},
    }
