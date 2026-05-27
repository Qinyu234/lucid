def validate_shared_categories_util(which: str = "all"):
    compiler = frozenset({"lib", "logging", "validate", "io_tree"})
    user = frozenset({"logging", "validate", "lib", "io", "debug"})
    if which == "compiler":
        return compiler
    if which == "user":
        return user
    return compiler | user
