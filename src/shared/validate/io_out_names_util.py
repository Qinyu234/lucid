def io_out_names_util(io: dict) -> list:
    from src.shared.validate.io_normalize_util import io_normalize_util
    return [f['name'] for f in io_normalize_util(io).get('out', [])]
