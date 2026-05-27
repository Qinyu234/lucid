def verify_shared_code(code: str, module_name: str, *, user_project: bool = False) -> tuple:
    from src.shared.validate.verify_shared_code_util import verify_shared_code_util

    return verify_shared_code_util(code, module_name, user_project=user_project)
