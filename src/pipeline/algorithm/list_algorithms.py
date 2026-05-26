def list_algorithms(profile_id: str | None=None, category: str | None=None, limit: int=12) -> list:
    from src.pipeline.algorithm.load_index import load_index
    index = load_index()
    items = list(index.get('algorithms', {}).values())
    if profile_id:
        items = [x for x in items if (x.get('fixed_task') or {}).get('profile_id') == profile_id]
    if category:
        items = [x for x in items if x.get('category') == category]
    items.sort(key=lambda x: x.get('function_name', ''))
    return items[:limit]
