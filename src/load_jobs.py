def load_jobs(path: str='io/input/idea_list.json') -> dict:
    from src.shared.lib.load_jobs_util import load_jobs_util

    return load_jobs_util(path)
