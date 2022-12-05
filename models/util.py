import os


def chain(input, functions: list[callable]):
    """
    Let functions be [f1, f2, f3, ...]
    Apply them in this order, that is return f3(f2(f1(input)))
    """
    if len(functions) > 0:
        first_function = functions[0]
        last_functions = functions[1:]
        return chain(first_function(input), last_functions)
    else:
        return input


def get_data_file_path(filename: str):
    return os.path.join(os.path.dirname(__file__), "../data/", filename)
