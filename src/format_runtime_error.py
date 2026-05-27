def format_runtime_error(exc):
    return {
        "ok": False,
        "code": "RUNTIME_ERROR",
        "message": str(exc),
        "detail": {},
    }
