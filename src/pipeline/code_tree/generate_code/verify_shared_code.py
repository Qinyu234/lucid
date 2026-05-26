def verify_shared_code(code: str, module_name: str) -> tuple:
    from src.import_rules.verify_generated_code import verify_generated_code
    return verify_generated_code(code, module_name, 'shared')
