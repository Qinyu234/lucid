import json
from pathlib import Path
from dataclasses import dataclass, field

from src.config.load_app_config import load_app_config

_SCHEMA_CACHE: dict[str, dict] = {}

_REF_MAP = {
    "job": "job_schema.json",
    "io_spec": "io_spec_schema.json",
    "io_field": "io_field.json",
}


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str] = field(default_factory=list)

    def fail(self, msg: str):
        self.ok = False
        self.errors.append(msg)


def _schema_dir() -> Path:
    cfg = load_app_config()
    return Path(cfg.get("schema_dir", "io/schema"))


def load_schema(name: str) -> dict:
    if name in _SCHEMA_CACHE:
        return _SCHEMA_CACHE[name]

    path = _schema_dir() / name
    if not path.exists():
        raise FileNotFoundError(f"[SCHEMA] not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    _SCHEMA_CACHE[name] = schema
    return schema


def _resolve_schema(schema: dict) -> dict:
    ref = schema.get("ref")
    if ref:
        file_name = _REF_MAP.get(ref, f"{ref}_schema.json")
        return load_schema(file_name)
    return schema


def validate(value, schema: dict, path: str = "$") -> ValidationResult:
    result = ValidationResult(ok=True)
    schema = _resolve_schema(schema)
    _validate_value(value, schema, path, result)
    return result


def _validate_value(value, schema: dict, path: str, result: ValidationResult):

    if "ref" in schema:
        return _validate_value(value, _resolve_schema(schema), path, result)

    expected_type = schema.get("type")

    if isinstance(expected_type, list):
        if not any(_check_type(value, t) for t in expected_type):
            result.fail(f"{path}: type mismatch, expected {expected_type}")
        return

    if expected_type and not _check_type(value, expected_type):
        result.fail(f"{path}: expected {expected_type}")
        return

    if expected_type == "object":
        if not isinstance(value, dict):
            result.fail(f"{path}: must be object")
            return

        for key in schema.get("required", []):
            if key not in value:
                result.fail(f"{path}: missing required '{key}'")

        for key, prop_schema in schema.get("properties", {}).items():
            if key in value:
                _validate_value(value[key], prop_schema, f"{path}.{key}", result)

        for key, default in schema.get("defaults", {}).items():
            if key not in value or value[key] == "":
                value[key] = default

    elif expected_type == "array":
        if not isinstance(value, list):
            result.fail(f"{path}: must be array")
            return

        min_items = schema.get("minItems")
        max_items = schema.get("maxItems")
        if min_items is not None and len(value) < min_items:
            result.fail(f"{path}: minItems {min_items}")
        if max_items is not None and len(value) > max_items:
            result.fail(f"{path}: maxItems {max_items}")

        item_schema = schema.get("items")
        if item_schema:
            for i, item in enumerate(value):
                _validate_value(item, item_schema, f"{path}[{i}]", result)

    elif expected_type == "string":
        if not isinstance(value, str):
            result.fail(f"{path}: must be string")
            return
        min_len = schema.get("minLength")
        if min_len is not None and len(value) < min_len:
            result.fail(f"{path}: minLength {min_len}")
        enum = schema.get("enum")
        if enum is not None and value not in enum:
            result.fail(f"{path}: not in enum")

    elif expected_type == "number":
        if not isinstance(value, (int, float)):
            result.fail(f"{path}: must be number")


def _check_type(value, t: str) -> bool:
    if t == "string":
        return isinstance(value, str)
    if t == "object":
        return isinstance(value, dict)
    if t == "array":
        return isinstance(value, list)
    if t == "number":
        return isinstance(value, (int, float))
    if t == "null":
        return value is None
    return True
