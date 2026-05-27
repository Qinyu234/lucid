def run_one_job(job_id):
    from src.load_jobs import load_jobs
    from src.pipeline import pipeline
    from src.shared.logging.setup_util import setup_util

    setup_util(job_id)
    data = load_jobs()
    job = next((j for j in data.get("jobs", []) if j.get("id") == job_id), None)
    if not job:
        raise SystemExit(f"unknown job_id: {job_id}")
    return pipeline(job)
