from .log import get_logger, log_event


def finish(context: dict) -> dict:

    logger = get_logger()
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

    log_event(
        logger,
        "runtime_summary",
        total=summary["total"],
        done=ok_count,
        error=err_count,
        incomplete=incomplete,
    )

    return summary
