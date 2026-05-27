def conftest_setup(job, job_id=None):
    from .generate_test import ensure_conftest

    return ensure_conftest(job, job_id=job_id)
