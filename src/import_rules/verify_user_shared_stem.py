def verify_user_shared_stem(module_stem: str) -> tuple:
    from src.import_rules.user_shared_allowlist import is_allowed_user_shared_stem

    if module_stem == "__init__":
        return True, ""
    if is_allowed_user_shared_stem(module_stem):
        return True, ""
    return (
        False,
        f"shared module {module_stem!r} not in §3.1 allowlist "
        f"(use logging/types/error/debug/profile/time/id/path/file/lib_*/validate_*)",
    )
