def validator_util(data: dict) -> dict:
    from src.shared.lib.deepcopy_util import deepcopy_util
    from src.shared.lib.schema_util import schema_util
    from src.shared.validate.job_input_util import job_input_util
    from src.shared.validate.schema_util import schema_util as validate_schema_util

    def error_packet(code: str, message: str) -> dict:
        return {"ok": False, "code": code, "message": message, "detail": {}}

    def fail(msg: str) -> dict:
        packet = error_packet("VALIDATION_ERROR", msg)
        packet["valid"] = False
        packet["data"] = None
        return packet

    if not isinstance(data, dict):
        return fail("root not dict")
    result = job_input_util(data)
    if not result.ok:
        return fail("; ".join(result.errors))

    normalized = deepcopy_util(data)
    job_schema = schema_util("job_schema.json")
    for i, job in enumerate(normalized.get("jobs") or []):
        job_result = validate_schema_util(job, job_schema, path=f"$.jobs[{i}]")
        if not job_result.ok:
            return fail("; ".join(job_result.errors))
    return {"valid": True, "data": normalized}

