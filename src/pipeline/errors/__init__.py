from .error_packet import error_packet
from .exceptions import exceptions


def errors(ctx=None):
    ns = type("_ErrorsNS", (), {})()
    ns.error_packet = error_packet
    ns.PipelineError = exceptions()
    return ns
