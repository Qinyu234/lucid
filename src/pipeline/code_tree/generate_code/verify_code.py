def verify_code(code: str, node: dict) -> tuple:
    from src.shared.validate.verify_code_util import verify_code_util

    return verify_code_util(code, node)
