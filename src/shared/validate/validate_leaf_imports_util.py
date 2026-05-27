def validate_leaf_imports_util(tree, shared_root="src.shared") -> tuple:
    from src.shared.validate.validate_leaf_file_imports_util import (
        validate_leaf_file_imports_util,
    )

    del shared_root
    return validate_leaf_file_imports_util(tree)
