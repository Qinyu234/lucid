def append_tokens(inputs: dict, meta: dict) -> dict:
    item = inputs.get("item")
    accumulator = inputs.get("accumulator", [])
    
    if item is None:
        raise ValueError("input 'item' is required and cannot be None")
    if not isinstance(item, str):
        raise TypeError(f"input 'item' must be string, got {type(item).__name__}")
    if not isinstance(accumulator, list):
        raise TypeError(f"input 'accumulator' must be list, got {type(accumulator).__name__}")
    
    tokens = item.split(" ")
    new_accumulator = accumulator + [tokens]
    
    return {"tokens": tokens, "accumulator": new_accumulator}
