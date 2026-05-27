def path_write_text_util(path: str, text: str, encoding: str = "utf-8") -> None:
    from pathlib import Path

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding=encoding)

