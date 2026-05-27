def ensure_job_scaffold_util(job: dict) -> None:
    import json
    from datetime import datetime, timezone
    from pathlib import Path

    root = Path(job["root_path"])
    job_id = job.get("id") or "project"

    def write_if_missing(path: Path, content: str) -> None:
        if path.exists():
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    (root / "io").mkdir(parents=True, exist_ok=True)
    (root / "requirement").mkdir(parents=True, exist_ok=True)
    (root / "tree" / "history").mkdir(parents=True, exist_ok=True)
    (root / "src" / "shared").mkdir(parents=True, exist_ok=True)
    (root / "src" / job_id).mkdir(parents=True, exist_ok=True)
    write_if_missing(root / "requirement" / "requirements.txt", "# project dependencies\n")
    write_if_missing(
        root / "run.py",
        f'# Project entry: calls src root package interface.\n\nfrom src.{job_id} import {job_id}\n\n\ndef run():\n    ctx = {{"data": {{}}, "meta": {{}}, "state": {{}}, "error": None}}\n    return {job_id}(ctx)\n\n\nif __name__ == "__main__":\n    run()\n',
    )
    write_if_missing(
        root / "src" / "__init__.py",
        "# Top-level src package.\n\n\ndef src(ctx):\n    return ctx\n",
    )
    write_if_missing(
        root / "src" / job_id / "__init__.py",
        f"# Root package interface for {job_id}.\n\n\ndef {job_id}(ctx):\n    return ctx\n",
    )
    write_if_missing(
        root / "src" / "shared" / "__init__.py",
        "# Shared root package.\n\n\ndef shared(ctx):\n    return ctx\n",
    )

    def write_category_init(category: str) -> None:
        write_if_missing(
            root / "src" / "shared" / category / "__init__.py",
            f"# shared/{category}/ package interface.\n\n\ndef {category}(ctx):\n    return ctx\n",
        )

    for cat in ("logging", "validate", "lib", "io", "debug"):
        write_category_init(cat)

    write_if_missing(
        root / "src" / "shared" / "logging" / "logging_util.py",
        '# Category: logging\nimport logging\n\n\ndef logging_util(ctx):\n    meta = ctx.setdefault("meta", {})\n    name = meta.get("logger_name", "app")\n    if "logger" not in meta:\n        meta["logger"] = logging.getLogger(name)\n    return ctx\n',
    )
    write_if_missing(
        root / "src" / "shared" / "validate" / "types_util.py",
        '# Category: validate (ctx data types)\n\ndef types_util(ctx):\n    data = ctx.setdefault("data", {})\n    for key, value in list(data.items()):\n        if value is not None and not isinstance(value, (str, int, float, bool, list, dict)):\n            ctx["error"] = f"invalid type for {key}"\n            break\n    return ctx\n',
    )
    write_if_missing(
        root / "src" / "shared" / "validate" / "error_util.py",
        '# Category: validate (error shape)\n\ndef error_util(ctx):\n    err = ctx.get("error")\n    if err is not None and not isinstance(err, (str, dict)):\n        ctx["error"] = {"message": str(err)}\n    return ctx\n',
    )
    write_if_missing(
        root / "src" / "shared" / "debug" / "debug_util.py",
        '# Category: debug probe\n\ndef debug_util(ctx):\n    meta = ctx.setdefault("meta", {})\n    meta.setdefault("debug", False)\n    return ctx\n',
    )
    write_if_missing(
        root / "src" / "shared" / "debug" / "profile_util.py",
        '# Category: performance probe\nimport time\n\n\ndef profile_util(ctx):\n    state = ctx.setdefault("state", {})\n    probes = state.setdefault("profile", {})\n    probes["t0"] = time.perf_counter()\n    return ctx\n',
    )
    write_if_missing(
        root / "src" / "shared" / "lib" / "time_util.py",
        '# Category: lib (time)\nfrom datetime import datetime, timezone\n\n\ndef time_util(ctx):\n    meta = ctx.setdefault("meta", {})\n    meta.setdefault("now_iso", datetime.now(timezone.utc).isoformat())\n    return ctx\n',
    )
    write_if_missing(
        root / "src" / "shared" / "lib" / "id_util.py",
        '# Category: lib (id)\nimport uuid\n\n\ndef id_util(ctx):\n    meta = ctx.setdefault("meta", {})\n    meta.setdefault("run_id", str(uuid.uuid4()))\n    return ctx\n',
    )
    write_if_missing(
        root / "src" / "shared" / "io" / "path_util.py",
        '# Category: io path (project io/ only)\nfrom pathlib import Path\n\n\ndef path_util(ctx):\n    meta = ctx.setdefault("meta", {})\n    root = Path(meta.get("project_root") or ".").resolve()\n    io_root = (root / "io").resolve()\n    meta["io_root"] = str(io_root)\n    return ctx\n',
    )
    write_if_missing(
        root / "src" / "shared" / "io" / "file_util.py",
        '# Category: io file read (under io_root only)\nfrom pathlib import Path\n\n\ndef file_util(ctx):\n    meta = ctx.setdefault("meta", {})\n    data = ctx.setdefault("data", {})\n    rel = data.get("io_read_rel")\n    if not rel:\n        return ctx\n    io_root = Path(meta.get("io_root") or Path(".").resolve() / "io").resolve()\n    target = (io_root / str(rel)).resolve()\n    if target != io_root and io_root not in target.parents:\n        ctx["error"] = "io_read outside io/"\n        return ctx\n    if target.is_file():\n        data["io_read_text"] = target.read_text(encoding="utf-8")\n    return ctx\n',
    )
    latest = root / "tree" / "latest.json"
    if not latest.exists():
        stamp = datetime.now(timezone.utc).isoformat()
        payload = {
            "updated": stamp,
            "stage": "scaffold",
            "status": "pending",
            "issues": [],
            "job_id": job_id,
            "goal": job.get("goal", ""),
            "root_path": str(root).replace("\\", "/"),
            "tree": {
                "function_name": job_id,
                "semantic": job.get("goal", ""),
                "children": [],
                "status": "growing",
                "topology": None,
                "io": {"in": [], "out": []},
                "code_path": str(root).replace("\\", "/"),
            },
        }
        write_if_missing(latest, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
