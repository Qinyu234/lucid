def extract_json_object(text: str) -> dict | None:
    from src.shared.validate.extract_json_object_util import extract_json_object_util

    return extract_json_object_util(text)
