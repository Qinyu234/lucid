"""Exception types for pipeline (exempt: multiple classes)."""


class PipelineError(Exception):
    code = "PIPELINE_ERROR"

    def __init__(self, message: str, detail: dict | None = None):
        super().__init__(message)
        self.message = message
        self.detail = detail or {}

    def to_packet(self) -> dict:
        from .error_packet import error_packet

        return error_packet(self.code, self.message, self.detail)


class ValidationError(PipelineError):
    code = "VALIDATION_ERROR"


class SchemaError(PipelineError):
    code = "SCHEMA_ERROR"


class LLMError(PipelineError):
    code = "LLM_ERROR"


class IOError(PipelineError):
    code = "IO_ERROR"


def exceptions():
    return PipelineError
