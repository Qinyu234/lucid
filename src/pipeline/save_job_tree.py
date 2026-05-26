def save_job_tree(root: dict, job: dict, stage: str, *, status: str | None=None, issues: list | None=None, extra: dict | None=None, job_id: str | None=None):
    import json
    from datetime import datetime, timezone
    from pathlib import Path

    from src.pipeline.tree_dir import tree_dir
    from src.shared.feature_enabled import feature_enabled
    from src.shared.get_logger import get_logger
    from src.shared.load_app_config import load_app_config
    from src.shared.log_event import log_event

    def _trim_history(history_dir: Path, max_files: int):
        if max_files <= 0 or not history_dir.exists():
            return
        files = sorted(history_dir.glob('*.json'), key=lambda p: p.stat().st_mtime)
        while len(files) > max_files:
            files.pop(0).unlink(missing_ok=True)
    cfg = load_app_config().get('tree_store', {})
    if not cfg.get('enabled', True):
        return None
    logger = get_logger(job_id or job.get('id'))
    out_dir = tree_dir(job)
    payload = {'updated': datetime.now(timezone.utc).isoformat(), 'stage': stage, 'status': status, 'issues': issues or [], 'job_id': job.get('id'), 'goal': job.get('goal'), 'root_path': job.get('root_path'), 'tree': root}
    if extra:
        payload.update(extra)
    latest = out_dir / 'latest.json'
    with latest.open('w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    if cfg.get('keep_history', True) and feature_enabled('tree_keep_history'):
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        hist = out_dir / 'history' / f'{stamp}_{stage}.json'
        hist.parent.mkdir(parents=True, exist_ok=True)
        with hist.open('w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        _trim_history(out_dir / 'history', int(cfg.get('max_history', 100)))
    log_event(logger, 'tree_saved', stage=stage, path=str(latest))
    return latest
