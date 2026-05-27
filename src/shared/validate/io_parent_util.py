def io_parent_util(parent: dict, child: dict) -> list:
    from src.shared.validate.io_link_util import io_link_util
    'Parent package boundary vs direct child io.'
    return io_link_util(parent.get('io'), child.get('io'), label='parent->child')
