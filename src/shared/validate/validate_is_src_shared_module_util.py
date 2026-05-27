def validate_is_src_shared_module_util(module=None, leaf_direct=False):
    from src.shared.validate.validate_shared_categories_util import validate_shared_categories_util

    categories = validate_shared_categories_util("all")
    prefix = "src.shared"
    if not module:
        return False
    if not (module == prefix or module.startswith(f"{prefix}.")):
        return False
    if not leaf_direct:
        return True
    if module == prefix:
        return True
    suffix = module[len(prefix) + 1 :]
    parts = suffix.split(".")
    if len(parts) == 2 and parts[0] in categories:
        return True
    if len(parts) == 1 and parts[0]:
        return True
    return False
