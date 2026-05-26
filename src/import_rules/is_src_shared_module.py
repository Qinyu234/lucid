def is_src_shared_module(module=None, leaf_direct=False):
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
    return "." not in suffix
