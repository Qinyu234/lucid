def ensure_conftest(job: dict | None, job_id=None):
    from pathlib import Path

    from src.pipeline.code_tree import write_file
    from src.shared.lib.app_config_util import app_config_util
    from src.shared.logging.event_util import event_util
    from src.shared.logging.get_logger_util import get_logger_util

    from .render_conftest import render_conftest
    from .tests_enabled import tests_enabled

    if not tests_enabled() or not job:
        return
    cfg = app_config_util().get("tests", {})
    if not cfg.get("write_conftest", True):
        return
    root_path = job.get("root_path")
    if not root_path:
        return
    path = Path(root_path) / "conftest.py"
    if path.exists():
        return
    write_file(str(path), render_conftest())
    event_util(get_logger_util(job_id), "code_tree_write_conftest", path=str(path))
