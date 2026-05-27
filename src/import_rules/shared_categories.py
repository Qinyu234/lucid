"""Category subpackages under `src/shared/` (one level: shared/<category>/<module>.py)."""

COMPILER_SHARED_CATEGORIES = frozenset({"lib", "logging", "validate", "io_tree"})

USER_SHARED_CATEGORIES = frozenset({"logging", "validate", "lib", "io", "debug"})

ALL_SHARED_CATEGORIES = COMPILER_SHARED_CATEGORIES | USER_SHARED_CATEGORIES
