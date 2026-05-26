def load_jobs(path: str='io/input/idea_list.json') -> dict:
    import json
    from pathlib import Path

    from src.pipeline.errors.exceptions import IOError
    from src.shared.get_logger import get_logger

    logger = get_logger()
    file_path = Path(path)
    if not file_path.exists():
        logger.error('input file not found: %s', file_path)
        raise IOError(f'file not found: {file_path}')
    try:
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        logger.error('invalid JSON: %s', exc)
        raise IOError(f'invalid JSON format: {exc}') from exc
    except Exception as exc:
        logger.exception('unexpected read error')
        raise IOError(f'unexpected error: {exc}') from exc
    logger.info('loaded input %s jobs=%s', file_path, len(data.get('jobs', [])))
    return data
