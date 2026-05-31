def input(inputs: dict, meta: dict) -> dict:
    # params["value"] is the value provided by the user in the graph
    params = meta.get("params", {})
    value = params.get("value")
    return {"value": value}
