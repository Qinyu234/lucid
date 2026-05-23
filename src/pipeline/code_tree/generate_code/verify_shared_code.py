from src.import_rules import verify_generated_code


def verify_shared_code(code: str, module_name: str) -> tuple:
    return verify_generated_code(code, module_name, "shared")
