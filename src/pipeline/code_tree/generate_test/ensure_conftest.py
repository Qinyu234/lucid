def ensure_conftest(job: dict | None, job_id=None):
    from src.shared.lib.ensure_conftest_util import ensure_conftest_util

    ensure_conftest_util(job, job_id)
