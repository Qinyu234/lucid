def validate_user_shared_stem_util(module_stem: str) -> tuple:
    allowed = frozenset(
        {
            "logging_util",
            "types_util",
            "error_util",
            "debug_util",
            "profile_util",
            "time_util",
            "id_util",
            "path_util",
            "file_util",
            "ctx_util",
        }
    )

    def _is_allowed(stem: str) -> bool:
        if stem in allowed:
            return True
        if stem.startswith("lib_") and stem.endswith("_util"):
            return True
        if stem.startswith("validate_") and stem.endswith("_util"):
            return True
        if stem.startswith("io_") and stem.endswith("_util"):
            return True
        if stem.startswith("logging_") and stem.endswith("_util"):
            return True
        return False

    if module_stem == "__init__":
        return True, ""
    if _is_allowed(module_stem):
        return True, ""
    return (
        False,
        f"shared module {module_stem!r} not in §3.1 allowlist "
        f"(use logging/types/error/debug/profile/time/id/path/file/lib_*/validate_*)",
    )
