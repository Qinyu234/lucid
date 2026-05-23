from pathlib import Path

from src.config.load_app_config import load_app_config
from src.log.get_logger import get_logger
from src.log.log_event import log_event

from ..write_file import write_file
from .render_conftest import render_conftest
from .tests_enabled import tests_enabled


def ensure_conftest(job: dict | None, job_id=None):
    if not tests_enabled() or not job:
        return

    cfg = load_app_config().get("tests", {})
    if not cfg.get("write_conftest", True):
        return

    root_path = job.get("root_path")
    if not root_path:
        return

    path = Path(root_path) / "conftest.py"
    if path.exists():
        return

    write_file(str(path), render_conftest())
    log_event(get_logger(job_id), "code_tree_write_conftest", path=str(path))
