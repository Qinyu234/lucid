from copy import deepcopy

from src.errors import error_packet
from src.schema.engine import load_schema, validate
from src.schema.validate_job_input import validate_job_input


def validator(data: dict) -> dict:
    def fail(msg: str) -> dict:
        packet = error_packet("VALIDATION_ERROR", msg)
        packet["valid"] = False
        packet["data"] = None
        return packet

    if not isinstance(data, dict):
        return fail("root not dict")

    result = validate_job_input(data)
    if not result.ok:
        return fail("; ".join(result.errors))

    normalized = deepcopy(data)
    job_schema = load_schema("job_schema.json")

    for i, job in enumerate(normalized["jobs"]):
        job_result = validate(job, job_schema, path=f"$.jobs[{i}]")
        if not job_result.ok:
            return fail("; ".join(job_result.errors))

    return {
        "valid": True,
        "data": normalized,
    }
