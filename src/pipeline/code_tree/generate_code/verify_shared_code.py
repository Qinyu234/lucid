def verify_shared_code(code: str, module_name: str, *, user_project: bool = False) -> tuple:
    from src.import_rules.verify_generated_code import verify_generated_code
    from src.import_rules.verify_user_shared_stem import verify_user_shared_stem

    if user_project:
        ok, msg = verify_user_shared_stem(module_name)
        if not ok:
            return ok, msg
    return verify_generated_code(code, module_name, "shared")
