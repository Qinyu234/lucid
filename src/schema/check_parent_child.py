from src.schema.check_io_link import check_io_link


def check_parent_child(parent: dict, child: dict) -> list:
    """Parent package boundary vs direct child io."""
    return check_io_link(parent.get("io"), child.get("io"), label="parent->child")
