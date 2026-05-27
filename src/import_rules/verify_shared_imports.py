def verify_shared_imports(tree):
    from src.import_rules.verify_shared_file_imports import verify_shared_file_imports

    return verify_shared_file_imports(tree)
