import os
import platform
from contextlib import suppress
from functools import wraps
from typing import Any, Union
from datetime import datetime


def denying_os(os_name) -> Any:
    """Decorator to ban an operating system from software through os.name.

    >>> import snakypy
    >>> @snakypy.helpers.utils.decorators.denying_os("posix")
    >>> def foo(): print("Hi")
    >>> foo()

    or using from

    >>> from snakypy.helpers.utils.decorators import denying_os
    >>> @denying_os("posix")
    >>> def foo(): print("Hi")
    >>> foo()

    Arguments:
        **os_name** {str} - You must receive the os.name of the operating system to be banned.
                            Windows = nt
                            Linux/Mac OS = posix
    """

    def decorator(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if os.name == os_name:
                msg = f"This software is not compatible with this ({os_name}) operating system."
                raise Exception(msg)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def only_linux(func: Any) -> Any:
    """
    A decorator to force a function or method to run on Unix systems only.

    Arguments:
        **func (Any):** Must be assigned a role.

    >>> import snakypy
    >>> @snakypy.helpers.utils.decorators.only_linux
    >>> def foo(): print("Hi")
    >>> foo()

    or using from

    >>> from snakypy.helpers.utils.decorators import only_linux
    >>> @only_linux
    >>> def foo(): print("Hi")
    >>> foo()
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not platform.system() == "Linux":
            msg = (
                "Invalid operating system. "
                f'This function "{func.__name__}" is only compatible with '
                "Linux systems."
            )
            raise Exception(msg)
        return func(*args, **kwargs)

    return wrapper


def runtime(func: Any) -> Any:
    """Decorator to test runtime others functions.

    Returns:
        str: Return print
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        context = func(*args, **kwargs)
        print(f"Time taken: {datetime.now() - start_time}")
        return context

    return wrapper


def silent_errors(func: Any) -> Any:
    @wraps(func)
    def wrapper(*args, **kwargs):
        with suppress(Exception):
            return func(*args, **kwargs)

    return wrapper


__all__ = ["only_linux", "denying_os", "runtime", "silent_errors"]
