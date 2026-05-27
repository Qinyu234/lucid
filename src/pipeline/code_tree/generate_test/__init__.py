from .ensure_conftest import ensure_conftest
from .verify_test import verify_test
from .write_leaf_test import write_leaf_test

def generate_test(node: dict, job: dict | None=None, job_id=None) -> bool:
    ensure_conftest(job, job_id=job_id)
    return write_leaf_test(node, job_id=job_id)
