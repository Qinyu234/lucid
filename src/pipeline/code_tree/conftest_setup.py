def conftest_setup(job, job_id=None):
    from src.pipeline.code_tree.generate_test.ensure_conftest import ensure_conftest

    return ensure_conftest(job, job_id=job_id)
