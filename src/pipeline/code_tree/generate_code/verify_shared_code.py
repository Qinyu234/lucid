def verify_shared_code(code: str, module_name: str, *, user_project: bool = False) -> tuple:
    from src.shared.validate.validate_generated_code_util import validate_generated_code_util
    from src.shared.validate.validate_user_shared_stem_util import validate_user_shared_stem_util

    if user_project:
        ok, msg = validate_user_shared_stem_util(module_name)
        if not ok:
            return ok, msg
    return validate_generated_code_util(code, module_name, "shared")
