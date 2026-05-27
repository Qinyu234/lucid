def sample_values_util(type_name="", field_name=""):
    default_type = "any"
    type_samples = {
        "str": lambda name: f'"sample_{name}"' if name else '"sample"',
        "int": lambda _name: "1",
        "float": lambda _name: "1.0",
        "bool": lambda _name: "True",
        "bytes": lambda _name: 'b"sample"',
        "list": lambda _name: "[]",
        "dict": lambda _name: "{}",
        "any": lambda _name: "None",
    }
    typ = (type_name or default_type).strip().lower() or default_type
    factory = type_samples.get(typ, type_samples["any"])
    return factory(field_name or "value")
