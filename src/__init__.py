from .io import io
from .validator import validator
from .pipeline import pipeline
from .report import report
from .finish import finish


def src():

    # 1. read data
    data = io()

    # 2. validate data
    valid = validator(data)

    if not valid:

        return

    jobs = data["jobs"]

    for job in jobs:

        result = pipeline(job)

        report(job, result)

    finish()