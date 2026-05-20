def clean_tasks(tasks: list[dict]) -> list[dict]:
    valid = []

    for t in tasks:
        if (
            isinstance(t, dict)
            and "file_name" in t
            and isinstance(t["file_name"], str)
            and "functions" in t
            and isinstance(t["functions"], list)
            and "imports" in t
            and isinstance(t["imports"], list)
        ):
            valid.append(t)

    return valid