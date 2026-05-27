def verify_test(code: str, function_name: str) -> tuple:
    from src.shared.lib.verify_test_util import verify_test_util

    return verify_test_util(code, function_name)
