def run_one_job(job_id):
    import sys
    from pathlib import Path

    from src.load_jobs import load_jobs
    from src.pipeline import pipeline
    from src.shared.setup_logging import setup_logging

    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    setup_logging(job_id)
    data = load_jobs()
    job = next((j for j in data.get("jobs", []) if j.get("id") == job_id), None)
    if not job:
        raise SystemExit(f"unknown job_id: {job_id}")
    return pipeline(job)
