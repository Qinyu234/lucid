def is_src_shared_module(module=None, leaf_direct=False):
    from src.import_rules.shared_categories import ALL_SHARED_CATEGORIES

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
    if len(parts) == 2 and parts[0] in ALL_SHARED_CATEGORIES:
        return True
    # legacy flat modules in older generated workplaces (shared/<module>.py)
    if len(parts) == 1 and parts[0]:
        return True
    return False
