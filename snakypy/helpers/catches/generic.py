import re
from collections import defaultdict
from os import environ, popen
from os.path import getsize, isfile, splitext
from typing import Union

from snakypy.helpers.decorators import only_linux


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


@only_linux
def shell() -> str:
    """
    Function to get the currently activated shell.

    >>> from snakypy import helpers
    >>> helpers.catches.shell()
    'sh'

    Returns:
        [str] -- Returns the name of the current shell.
    """
    try:
        get_shell = environ["SHELL"]
    except KeyError:
        return ""

    if "/" in get_shell:
        return get_shell.strip("\n").strip("").split("/")[-1]

    return get_shell


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


def is_blank_file(filepath: str) -> bool:
    """
    Checks if a file is blank, that is, it does not contain lines.

    >>> from snakypy import helpers
    >>> file = '/tmp/text.txt'
    >>> helpers.catches.is_blank_file(file)
    'True'

    or

    >>> from snakypy.helpers.catches import is_blank_file
    >>> file = '/tmp/text.txt'
    >>> is_blank_file(file)
    'True'

    Args:
        filepath (str): Receive the file along with the full path

    Returns:
        [bool] -- Returns True if the file is blank, and False if it has content.
    """
    return isfile(filepath) and getsize(filepath) == 0


def is_palindrome(word: str) -> Union[bool, str]:
    """Function to check if word is a palindrome
    >>> from snakypy.helpers.catches import is_palindrome
    >>> is_palindrome("ana")
    True
    >>> from snakypy.helpers.catches import is_palindrome
    >>> is_palindrome("banana")
    False

    Args:
        word (str): Must receive a string

    Returns:
        [bool]: Return True if it is a palindrome, and False if it is not a palindrome.
    """
    try:

        # We make a slicing by traversing the word of the "word" parameter, backwards.
        slicing_reverse: str = word[::-1]

        # If the original word (parameter) is equal to the word traversed backwards,
        # then the return will be True
        if word == slicing_reverse:
            return True

        # If they are not identical it will always return False; which is not palindrome.
        return False

    except TypeError as err:
        return f"The parameter must be a string: {err}"


def turned_palindrome(word: str) -> Union[bool, str]:
    """Function to check if word can become a palindrome.

    >>> from snakypy.helpers.catches import turned_palindrome
    >>> turned_palindrome("aabbcc")
    True
    >>> from snakypy.helpers.catches import turned_palindrome
    >>> turned_palindrome("banana")
    False

    Args:
        word (str): Must receive a string.

    Returns:
        [bool]: Return True if the word can be a palindrome,
                and False if it cannot be a palindrome.
    """
    try:
        # Creates a map (dict) of type int, to store all characters
        # (and their counts) of the "word" parameter.
        # Model: defaultdict(int, {})
        map_: defaultdict = defaultdict(int)

        # For each letter of the "word" parameter, add a counter.
        # word = "aabbcc"
        # Model: defaultdict(int, {'a': 2, 'b': 2, 'c': 2})
        for letter in word:
            map_[letter] += 1

        # Creating a variable to store a temporary counter.
        count = 0

        # Scroll through the values (counters) of each letter.
        for value in map_.values():

            # Checks if the remainder of the division of the value of
            # each letter is equal to 1.
            if value % 2 == 1:
                count = count + 1

            # If the "count" is greater than 1, we no longer have a
            # word that could be palindrome.
            if count > 1:
                return False

        # It will always fall in this return if the variable "count"
        # is equal to or less than 1.
        return True

    except TypeError as err:
        return f"The parameter must be a string: {err}"


__all__ = [
    "whoami",
    "shell",
    "extension",
    "is_blank_file",
    "is_palindrome",
    "turned_palindrome",
]
