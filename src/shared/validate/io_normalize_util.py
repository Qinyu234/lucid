def io_normalize_util(raw) -> dict:
    from src.shared.validate.io_empty_util import io_empty_util
    default_type = 'any'

    def normalize_field(raw) -> dict | None:
        if isinstance(raw, str) and raw.strip():
            return {'name': raw.strip(), 'type': default_type}
        if isinstance(raw, dict):
            name = raw.get('name') or raw.get('key')
            if not name or not str(name).strip():
                return None
            typ = raw.get('type') or default_type
            return {'name': str(name).strip(), 'type': str(typ).strip() or default_type}
        return None

    def _normalize_side(raw) -> list:
        if not isinstance(raw, list):
            return []
        fields = []
        seen = set()
        for item in raw:
            field = normalize_field(item)
            if not field or field['name'] in seen:
                continue
            seen.add(field['name'])
            fields.append(field)
        fields.sort(key=lambda x: x['name'])
        return fields
    if not isinstance(raw, dict):
        return io_empty_util()
    if 'in' in raw or 'out' in raw:
        return {'in': _normalize_side(raw.get('in')), 'out': _normalize_side(raw.get('out'))}
    if 'data_keys' in raw:
        keys = _normalize_side(raw.get('data_keys'))
        return {'in': keys, 'out': keys}
    return io_empty_util()
