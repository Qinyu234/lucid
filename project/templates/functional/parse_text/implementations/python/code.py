def parse_text(inputs: dict, meta: dict) -> dict:
    text = inputs.get("text")
    separator = inputs.get("separator", " ")

    if text is None:
        raise ValueError("input 'text' is required and cannot be None")
    if not isinstance(text, str):
        raise TypeError(f"input 'text' must be string, got {type(text).__name__}")
    if not isinstance(separator, str):
        raise TypeError(f"input 'separator' must be string, got {type(separator).__name__}")

    if text == "":
        tokens = []
    else:
        tokens = text.split(separator)

    return { "tokens": tokens }
