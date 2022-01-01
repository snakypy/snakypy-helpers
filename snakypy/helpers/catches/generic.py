import re
from os.path import splitext


def extension(filename: str, dots: bool = False) -> str:
    """Get a file extension

    >>> from snakypy import helpers
    >>> file = '/tmp/file.tar.gz'
    >>> helpers.catches.extension(file)
    '.gz'
    >>> helpers.catches.extension(file, dots=True)
    'tar.gz'

    or

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


__all__ = ["extension"]
