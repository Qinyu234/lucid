def assess_job(root, job=None) -> tuple:
    from src.shared.lib.assess_job_util import assess_job_util

    return assess_job_util(root, job)
