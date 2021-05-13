import re
from os.path import splitext
from os import popen
from snakypy.helpers.utils.decorators import only_linux
from subprocess import check_output
from snakypy.helpers.utils import decorators
from sys import platform


@only_linux
def whoami() -> str:
    """
        Get the currently logged in user.

        >>> from snakypy import helpers
        >>> helpers.catches.whoami()
        'william'

    Returns:
         [str] -- Returns the name of the current user.
    """
    return str(popen("whoami").read()).replace("\n", "")


@decorators.only_linux
def shell() -> str:
    """
    Function to get the currently activated shell.

    >>> from snakypy import helpers
    >>> helpers.catches.shell()
    'sh'

    Returns:
        [str] -- Returns the name of the current shell.
    """
    if platform.startswith("win"):
        raise RuntimeError("Unsupported operating system.")

    s = check_output("echo $0", shell=True, universal_newlines=True)
    lst = s.strip("\n").strip("").split("/")

    return lst[2]


def extension(filename: str, dots: bool = False) -> str:
    """Get a file extension

    >>> from snakypy import helpers
    >>> file = '/tmp/file.tar.gz'
    >>> helpers.catches.extension(file)
    '.gz'
    >>> helpers.catches.extension(file, dots=True)
    'tar.gz'

    or using from

    >>> from snakypy.helpers.catches import extension
    >>> file = '/tmp/file.tar.gz'
    >>> extension(file)
    '.gz'
    >>> extension(file, dots=True)
    'tar.gz'

    Args:
        filename (str): Receives the file name or its full path

        dots (bool): If it is True, I return the extension from the first point found, that is, if the file has
                     more than one point, the first one will be the capture point, otherwise it will take the last
                     point found. (Default: False)

    Returns:
        [object] -- Returns a string containing the extension or None.
    """
    if dots:
        m = re.search(r"(?<=[^/\\]\.).*$", filename)
        if not m:
            raise TypeError("Invalid parameter type passed.")
        ext = m.group(0)
        return ext
    else:
        ext = splitext(filename)[1]
        if not ext:
            raise TypeError("Invalid parameter type passed.")
        return ext


__all__ = ["whoami", "shell", "extension"]
