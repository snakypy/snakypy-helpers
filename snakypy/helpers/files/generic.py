from contextlib import suppress
from datetime import datetime
from os.path import exists
from shutil import SameFileError, copyfile
from typing import Any, List, Union

from tomlkit import dumps, parse


def create_file(content: Any, file_path: str, force: bool = False) -> bool:
    """
    Create a text file.

    >>> import snakypy
    >>> snakypy.helpers.files.create_file('My file', '/tmp/file.txt')
    >>> snakypy.helpers.files.create_file('My file', '/tmp/file.txt', force=True)

    or using from

    >>> from snakypy.helpers.files import create_file
    >>> create_file('My file', '/tmp/file.txt')
    >>> create_file('My file', '/tmp/file.txt', force=True)

    Arguments:
        **content {str}** -- Reports a text or an object containing a text.

        **file_path {str}** -- You must receive the full absolute file path.

    Keyword Arguments:
        **force {bool}** -- Use the True option if you want to overwrite the existing file. (default: {False})

    Returns:
        **[bool]** -- If everything went well, it will return True.
    """

    if not force and exists(file_path):
        raise FileExistsError(
            f">>> The file {file_path} already exists, use force=True."
        )
    else:
        try:
            with open(file_path, "w") as f:
                f.write(content)
                return True
        except Exception as err:
            raise Exception(f">>> There was an error creating the file: {err}")


def read_file(file_path: str, split: bool = False) -> Union[str, List[str]]:
    """
    Reads a text file.

    >>> from snakypy import helpers
    >>> file = '/tmp/my_file.txt'
    >>> helpers.files.create_file('My content file', file, force=True)
    True
    >>> helpers.files.read_file(file)
    'My content file'

    Args:
        file_path (str): You must receive the full/absolute file path.

        split (bool): If this option is True, a list will be returned where
                                the breaks will be made using line skips. (default: {False})

    Returns:
        [str|list]: By default it returns a string. If the option split=True,
                    a list of line breaks will be returned.
    """
    try:
        with open(file_path) as f:
            if split:
                return f.read().split("\n")
            return f.read()
    except FileNotFoundError as err:
        raise FileNotFoundError(f'>>> File "{file_path}" does not exist. {err}')


def backup_file(
    origin: str, destiny: str, *, date: bool = False, extension: bool = True
) -> None:
    """
        Create backup of files with date and time.

        >>> from snakypy import helpers
        >>> helpers.files.backup_file("/tmp/file.txt", "/tmp/file.txt")
        >>> helpers.files.backup_file("/tmp/file.txt", "/tmp/file.txt", extension=False)
        >>> helpers.files.backup_file("/tmp/file.txt", "/tmp/file2.txt")
        >>> helpers.files.backup_file("/tmp/file.txt", "/tmp/file2.txt", date=True)

    Arguments:
        origin (str): Source location of the file.

        destiny (str): Destination location of the file.

        date (bool, optional): Adds date and time to the generated backup file name.
                                   If the source and destination have the same values by default, the
                                   date is incorporated in the backup file name.Defaults to False.

        extension (bool, optional): Adds the file extension in the name after the subtitle. Defaults to True.
    """

    ext = ""
    if extension:
        ext = f".{origin.split('.')[-1]}"
    destiny_format = destiny
    if date or origin == destiny and not date:
        destiny_format = f"{destiny}__BACKUP-{datetime.today().isoformat()}{ext}"
    with suppress(FileNotFoundError, SameFileError):
        copyfile(origin, destiny_format)


def eqversion(filepath, version, *, key=("tool", "poetry", "version")):
    """
        Function to update the version of the pyproject.toml file according to the version of __init__.py

    In __init__.py do:

    .. code-block:: python

        from snakypy.helpers.files import eqversion
        pyproject = join(dirname(abspath(__file__)), "..", "pyproject.toml")
        eqversion(pyproject, __version__)

        NOTE: In ".." it defines as much of the directory that wants to return.

    Args:
        filepath: File path "pyproject.toml".
        version: Enter the version found in the "__init__.py" file of the package.
        key: You must pass the key level to access the version on "pyproject.toml".
        By default, this value is used for Poetry.
    """
    with suppress(FileNotFoundError):
        parsed = parse(read_file(filepath))
        change = False

        if not len(key):
            raise KeyError(
                f'Error function "{eqversion.__name__}": Enter the access keys. '
                f'Must be a tuple. E.g: key=("key1", "key2",...)'
            )
        elif len(key) == 1:
            if parsed[key[0]] != version:
                parsed[key[0]] = version
                change = True
        elif len(key) == 2:
            if parsed[key[0]][key[1]] != version:
                parsed[key[0]][key[1]] = version
                change = True
        elif len(key) == 3:
            if parsed[key[0]][key[1]][key[2]] != version:
                parsed[key[0]][key[1]][key[2]] = version
                change = True
        elif len(key) == 4:
            if parsed[key[0]][key[1]][key[2]][key[3]] != version:
                parsed[key[0]][key[1]][key[2]][key[3]] = version
                change = True
        else:
            raise KeyError(
                f'Error function "{eqversion.__name__}": The number of supported keys has overflowed. Must be < 4.'
            )

        if change:
            create_file(dumps(parsed), filepath, force=True)


__all__ = ["read_file", "create_file", "backup_file", "eqversion"]
