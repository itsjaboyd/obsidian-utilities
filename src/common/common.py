"""General package containing commonly used classes, functions, 
    and other objects across the obsidian-utilities project. 
    Utilizing these across multiple packages makes testing 
    important to avoid things breaking unexpectedly.

    Author: Jason Boyd
    Date: January 22, 2025
    Modified: January 22, 2025
"""

import pathlib


def check_argument_iterable(supplied_object):
    try:  # recommended to just attempt iter() on object
        result = iter(supplied_object)
        return
    except:  # simply raise the exception that is met
        raise


def check_iterable_types(supplied_iterable, strict_type):
    check_argument_iterable(supplied_iterable)
    iterables_typed = []
    for iterated_object in supplied_iterable:
        iterables_typed.append(isinstance(iterated_object, strict_type))
    if not all(iterables_typed):
        exception_message = f"Not everything in {type(supplied_iterable)} "
        exception_message += f"is of {strict_type} type!"
        raise ValueError(exception_message)


def check_argument_type(supplied_object, strict_type):
    if not isinstance(supplied_object, strict_type):
        exception_message = f"Supplied argument {supplied_object} "
        exception_message += f"is not of {strict_type} type!"
        raise ValueError(exception_message)


def attempt_pathlike_extraction(supplied_object):
    if isinstance(supplied_object, pathlib.Path):
        return supplied_object

    try:  # attempt to convert supplied_object into pathlib.Path
        usable_object = pathlib.Path(supplied_object)
        return usable_object
    except:  # caller supplied something weird Path() is unable to deal with
        exception_message = f"Supplied argument {supplied_object} could "
        exception_message += "not be converted into path-like object!"
        raise ValueError(exception_message)
