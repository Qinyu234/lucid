def ensure_job_scaffold(job: dict) -> None:
    import json
    from datetime import datetime, timezone
    from pathlib import Path
    root = Path(job['root_path'])
    job_id = job.get('id') or 'project'

    def write_if_missing(path: Path, content: str) -> None:
        if path.exists():
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    (root / 'io').mkdir(parents=True, exist_ok=True)
    (root / 'requirement').mkdir(parents=True, exist_ok=True)
    (root / 'tree' / 'history').mkdir(parents=True, exist_ok=True)
    (root / 'src' / 'shared').mkdir(parents=True, exist_ok=True)
    write_if_missing(root / 'requirement' / 'requirements.txt', '# project dependencies\n')
    write_if_missing(root / 'run.py', f'# Project entry: calls src root package interface.\n\nfrom src.{job_id} import {job_id}\n\n\ndef run():\n    ctx = {{"data": {{}}, "meta": {{}}, "state": {{}}, "error": None}}\n    return {job_id}(ctx)\n\n\nif __name__ == "__main__":\n    run()\n')
    write_if_missing(root / 'src' / '__init__.py', '# Top-level src package.\n\n\ndef src(ctx):\n    return ctx\n')
    write_if_missing(root / 'src' / 'shared' / '__init__.py', '# Shared utilities: stdlib wrappers, typing, logging.\n\n\ndef shared(ctx):\n    return ctx\n')
    write_if_missing(root / 'src' / 'shared' / 'logging_util.py', 'import logging\n\n\ndef logging_util(ctx):\n    meta = ctx.setdefault("meta", {})\n    name = meta.get("logger_name", "app")\n    if "logger" not in meta:\n        meta["logger"] = logging.getLogger(name)\n    return ctx\n')
    write_if_missing(root / 'src' / 'shared' / 'ctx_util.py', 'def ctx_util(ctx):\n    ctx.setdefault("data", {})\n    ctx.setdefault("meta", {})\n    ctx.setdefault("state", {})\n    ctx.setdefault("error", None)\n    return ctx\n')
    latest = root / 'tree' / 'latest.json'
    if not latest.exists():
        stamp = datetime.now(timezone.utc).isoformat()
        payload = {'updated': stamp, 'stage': 'scaffold', 'status': 'pending', 'issues': [], 'job_id': job_id, 'goal': job.get('goal', ''), 'root_path': str(root).replace('\\', '/'), 'tree': {'function_name': job_id, 'semantic': job.get('goal', ''), 'children': [], 'status': 'growing', 'topology': None, 'io': {'in': [], 'out': []}, 'code_path': str(root).replace('\\', '/')}}
        write_if_missing(latest, json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    write_if_missing(root / 'src' / 'shared' / 'types_util.py', 'def types_util(ctx):\n    data = ctx.setdefault("data", {})\n    for key, value in list(data.items()):\n        if value is not None and not isinstance(value, (str, int, float, bool, list, dict)):\n            ctx["error"] = f"invalid type for {key}"\n            break\n    return ctx\n')
