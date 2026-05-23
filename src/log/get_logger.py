from src.log.setup_logging import setup_logging


def get_logger(job_id: str | None = None):
    return setup_logging(job_id)
