def get_logger_util(job_id=None):
    from src.shared.logging.setup_util import setup_util

    return setup_util(job_id)
