def validate(value, schema: dict, path: str='$'):
    from src.shared.load_schema import load_schema

    class ValidationResult:

        def __init__(self, ok: bool=True):
            self.ok = ok
            self.errors: list[str] = []

        def fail(self, msg: str):
            self.ok = False
            self.errors.append(msg)

    def check_type(value, t: str) -> bool:
        if t == 'string':
            return isinstance(value, str)
        if t == 'object':
            return isinstance(value, dict)
        if t == 'array':
            return isinstance(value, list)
        if t == 'number':
            return isinstance(value, (int, float))
        if t == 'null':
            return value is None
        return True

    def resolve_schema(schema: dict) -> dict:
        ref = schema.get('ref')
        if not ref:
            return schema
        file_name = f'{ref}_schema.json'
        if ref == 'job':
            file_name = 'job_schema.json'
        elif ref == 'io_spec':
            file_name = 'io_spec_schema.json'
        elif ref == 'io_field':
            file_name = 'io_field.json'
        return load_schema(file_name)

    def validate_value(value, schema: dict, path: str, result: ValidationResult):
        if 'ref' in schema:
            validate_value(value, resolve_schema(schema), path, result)
            return
        expected_type = schema.get('type')
        if isinstance(expected_type, list):
            if not any((check_type(value, t) for t in expected_type)):
                result.fail(f'{path}: type mismatch, expected {expected_type}')
            return
        if expected_type and (not check_type(value, expected_type)):
            result.fail(f'{path}: expected {expected_type}')
            return
        if expected_type == 'object':
            if not isinstance(value, dict):
                result.fail(f'{path}: must be object')
                return
            for key in schema.get('required', []):
                if key not in value:
                    result.fail(f"{path}: missing required '{key}'")
            for key, prop_schema in schema.get('properties', {}).items():
                if key in value:
                    validate_value(value[key], prop_schema, f'{path}.{key}', result)
            for key, default in schema.get('defaults', {}).items():
                if key not in value or value[key] == '':
                    value[key] = default
        elif expected_type == 'array':
            if not isinstance(value, list):
                result.fail(f'{path}: must be array')
                return
            min_items = schema.get('minItems')
            max_items = schema.get('maxItems')
            if min_items is not None and len(value) < min_items:
                result.fail(f'{path}: minItems {min_items}')
            if max_items is not None and len(value) > max_items:
                result.fail(f'{path}: maxItems {max_items}')
            item_schema = schema.get('items')
            if item_schema:
                for i, item in enumerate(value):
                    validate_value(item, item_schema, f'{path}[{i}]', result)
        elif expected_type == 'string':
            if not isinstance(value, str):
                result.fail(f'{path}: must be string')
                return
            min_len = schema.get('minLength')
            if min_len is not None and len(value) < min_len:
                result.fail(f'{path}: minLength {min_len}')
            enum = schema.get('enum')
            if enum is not None and value not in enum:
                result.fail(f'{path}: not in enum')
        elif expected_type == 'number':
            if not isinstance(value, (int, float)):
                result.fail(f'{path}: must be number')
    result = ValidationResult(ok=True)
    validate_value(value, resolve_schema(schema), path, result)
    return result
