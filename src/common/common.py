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
    """Check to see if a supplied argument is iterable.

    Args:
        supplied_object (any): the supplied argument to check.
    """

    try:  # recommended to just attempt iter() on object
        result = iter(supplied_object)
        return True
    except:  # simply raise the exception that is met
        raise


def check_iterable_types(supplied_iterable, strict_type):
    """Check to see if the supplied iterable contains objects that
        are all of the same type.

    Args:
        supplied_iterable (iterable): the iterable to check internal
            types against.
        strict_type (type): the type that all internal objects to the
            supplied iterable should match.

    Raises:
        ValueError: if any of the internal objects inside the supplied
            iterable do not match the supplied type.
    """

    check_argument_iterable(supplied_iterable)
    iterables_typed = []
    for iterated_object in supplied_iterable:
        iterables_typed.append(isinstance(iterated_object, strict_type))
    if not all(iterables_typed):
        exception_message = f"Not everything in {type(supplied_iterable)} "
        exception_message += f"is of {strict_type} type!"
        raise ValueError(exception_message)
    return True


def check_argument_type(supplied_object, strict_type):
    """Given an argument object, check to ensure it matches the supplied type.

    Args:
        supplied_object (any): the argument to check type against.
        strict_type (type): the type to match against the argument.

    Raises:
        ValueError: if the argument does not have the supplied type.
    """

    if not isinstance(supplied_object, strict_type):
        exception_message = f"Supplied argument {supplied_object} "
        exception_message += f"is not of {strict_type} type!"
        raise ValueError(exception_message)
    return True


def attempt_pathlike_extraction(supplied_object):
    """Given a path-like object, attempt to extract a pathlib.Path object
        out of the argument and return it. If the argument cannot be used
        as a Path() object then raise an exception.

    Args:
        supplied_object (any): the path-like object to test path-ness against.

    Raises:
        ValueError: if the argument cannot be turned into a Path() object.

    Returns:
        pathlib.Path: the extracted pathlib.Path object from the argument.
    """

    if isinstance(supplied_object, pathlib.Path):
        return supplied_object

    try:  # attempt to convert supplied_object into pathlib.Path
        usable_object = pathlib.Path(supplied_object)
        return usable_object
    except:  # caller supplied something weird Path() is unable to deal with
        exception_message = f"Supplied argument {supplied_object} could "
        exception_message += "not be converted into path-like object!"
        raise ValueError(exception_message)
