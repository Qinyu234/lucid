def validate_user_shared_category_util(category: str) -> bool:
    from src.shared.validate.validate_shared_categories_util import validate_shared_categories_util

    return category in validate_shared_categories_util("user")
