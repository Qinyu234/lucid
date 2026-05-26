def get_logger(job_id=None):
    from src.shared.setup_logging import setup_logging

    return setup_logging(job_id)
