"""Allowed `src/shared/<category>/*.py` stems for user-generated projects (codegen-user-contract §3.1)."""



from src.import_rules.shared_categories import USER_SHARED_CATEGORIES



USER_SHARED_STEMS = frozenset(

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





def is_allowed_user_shared_stem(stem: str) -> bool:

    if stem in USER_SHARED_STEMS:

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





def is_allowed_user_shared_category(category: str) -> bool:

    return category in USER_SHARED_CATEGORIES


