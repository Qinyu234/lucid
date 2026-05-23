DEFAULT_TYPE = "any"

_TYPE_SAMPLES = {
    "str": lambda name: f'"sample_{name}"' if name else '"sample"',
    "int": lambda _name: "1",
    "float": lambda _name: "1.0",
    "bool": lambda _name: "True",
    "bytes": lambda _name: 'b"sample"',
    "list": lambda _name: "[]",
    "dict": lambda _name: "{}",
    "any": lambda _name: "None",
}


def sample_values(type_name: str, field_name: str = "") -> str:
    typ = (type_name or DEFAULT_TYPE).strip().lower() or DEFAULT_TYPE
    factory = _TYPE_SAMPLES.get(typ, _TYPE_SAMPLES["any"])
    return factory(field_name or "value")
