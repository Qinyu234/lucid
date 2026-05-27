def finish(context: dict) -> dict:
    from src.shared.logging.get_logger_util import get_logger_util
    from src.shared.logging.event_util import event_util

    logger = get_logger_util()
    results = context.get("results", []) if context else []

    ok_count = sum(1 for r in results if r.get("result", {}).get("status") == "done")
    err_count = sum(1 for r in results if r.get("result", {}).get("status") == "error")
    incomplete = sum(1 for r in results if r.get("result", {}).get("status") == "incomplete")

    summary = {
        "status": "OK" if err_count == 0 else "PARTIAL",
        "total": len(results),
        "done": ok_count,
        "error": err_count,
        "incomplete": incomplete,
        "results": results,
    }

    event_util(
        logger,
        "runtime_summary",
        total=summary["total"],
        done=ok_count,
        error=err_count,
        incomplete=incomplete,
    )

    return summary
