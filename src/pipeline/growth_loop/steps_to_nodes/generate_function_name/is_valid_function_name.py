def is_valid_function_name(name):

    return (
        isinstance(name, str)
        and name.isidentifier()
        and not name[0].isdigit()
        and "__" not in name
    )
