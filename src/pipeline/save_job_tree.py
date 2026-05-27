def save_job_tree(
    root: dict,
    job: dict,
    stage: str,
    *,
    status: str | None = None,
    issues: list | None = None,
    extra: dict | None = None,
    job_id: str | None = None,
):
    import json
    from datetime import datetime, timezone
    from pathlib import Path

    from src.shared.lib.app_config_util import app_config_util
    from src.shared.lib.feature_util import feature_util
    from src.shared.lib.tree_dir_util import tree_dir_util
    from src.shared.logging.event_util import event_util
    from src.shared.logging.get_logger_util import get_logger_util

    def _trim_history(history_dir: Path, max_files: int) -> None:
        if max_files <= 0 or not history_dir.exists():
            return
        files = sorted(history_dir.glob("*.json"), key=lambda p: p.stat().st_mtime)
        while len(files) > max_files:
            files.pop(0).unlink(missing_ok=True)

    cfg = app_config_util().get("tree_store", {})
    if not cfg.get("enabled", True):
        return None
    logger = get_logger_util(job_id or job.get("id"))
    out_dir = Path(tree_dir_util(job))
    payload = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "stage": stage,
        "status": status,
        "issues": issues or [],
        "job_id": job.get("id"),
        "goal": job.get("goal"),
        "root_path": job.get("root_path"),
        "tree": root,
    }
    if extra:
        payload.update(extra)
    latest = out_dir / "latest.json"
    with latest.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    if cfg.get("keep_history", True) and feature_util("tree_keep_history"):
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        hist = out_dir / "history" / f"{stamp}_{stage}.json"
        hist.parent.mkdir(parents=True, exist_ok=True)
        with hist.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        _trim_history(out_dir / "history", int(cfg.get("max_history", 100)))
    event_util(logger, "tree_saved", stage=stage, path=str(latest))
    return latest
