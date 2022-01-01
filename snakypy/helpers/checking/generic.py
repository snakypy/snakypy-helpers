import os
import platform
import stat
from collections import defaultdict
from os import environ, popen
from os.path import getsize, isfile
from typing import Union, no_type_check

from snakypy.helpers.decorators import denying_os


@denying_os("Windows", is_func=True)
def whoami() -> str:
    """
        Get the currently logged in user.

        >>> from snakypy import helpers
        >>> helpers.checking.whoami()
        'william'

    Returns:
         [str] -- Returns the name of the current user.
    """
    return str(popen("whoami").read()).replace("\n", "")


@denying_os("Windows", is_func=True)
def shell() -> str:
    """
    Function to get the currently activated shell.

    >>> from snakypy import helpers
    >>> helpers.checking.shell()
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


def is_blank_file(filepath: str) -> bool:
    """
    Checks if a file is blank, that is, it does not contain lines.

    >>> from snakypy import helpers
    >>> file = '/tmp/text.txt'
    >>> helpers.checking.is_blank_file(file)
    'True'

    or

    >>> from snakypy.helpers.checking import is_blank_file
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
    >>> from snakypy.helpers.checking import is_palindrome
    >>> is_palindrome("ana")
    True
    >>> from snakypy.helpers.checking import is_palindrome
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

    >>> from snakypy.helpers.checking import turned_palindrome
    >>> turned_palindrome("aabbcc")
    True
    >>> from snakypy.helpers.checking import turned_palindrome
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


@no_type_check
def is_hidden(filepath: str) -> Union[bool, None]:
    """
        Checks if a file or folder is hidden

        .. code-block:: python

            from snakypy.helpers.checking import is_hidden
            is_hidden("/home/user/.bashrc")

    Args:
        filepath (str):

    Returns:
        Bool or None
    """
    if platform.system() == "Windows":
        state = bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
        return state
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        dot = filepath.split("/")[-1][0]
        return True if dot == "." else False
    return None


__all__ = [
    "shell",
    "whoami",
    "is_blank_file",
    "is_palindrome",
    "turned_palindrome",
    "is_hidden",
]
