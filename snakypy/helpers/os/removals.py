from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from os import listdir, remove, rmdir, walk
from os.path import isdir, join
from shutil import rmtree
from typing import Any


def remove_objects(*, objects: tuple = ()) -> None:
    """
        Removes files or folders.

        >>> from snakypy.helpers.os import remove_objects
        >>> remove_objects(objects=("/tmp/folder", "/tmp/file.txt"))

    Args:
        objects (tuple): It must receive the path of the object, folders or files.

    Returns:
        None
    """
    with suppress(FileNotFoundError):
        for item in objects:
            rmtree(item, ignore_errors=True) if isdir(item) else remove(item)


def rmdir_blank(path: str) -> None:
    """
    Removes folders recursively if they are empty from a
    certain path.

    >>> from snakypy import helpers
    >>> helpers.os.rmdir_blank("/tmp/program_x")

    Args:
        path (str): Must receive a string in the form of path.
    """
    for r, d, f in walk(path, topdown=False):
        for folder in d:
            if len(listdir(join(r, folder))) == 0:
                try:
                    rmdir(join(r, folder))
                except PermissionError:
                    raise PermissionError("No permission to remove empty folders")
                except Exception:
                    raise Exception("It was not possible to clean empty folders.")


def cleaner(directory, *file: Any, level: int = 0) -> int:
    """
        **DANGER!** A function for cleaning objects and folders on the system.

        >>> from snakypy import helpers
        >>> helpers.os.cleaner("/tmp/foo", level=1)
        1
        >>> helpers.os.cleaner("/tmp/foo", level=2)
        2
        >>> helpers.os.cleaner("/tmp/foo", "bar.txt")

        Args:
            directory (str): Directory where are the files to be destroyed

            file (Any): Enter an N file name number (Optional)

            level (int): This option receives 3 values, they are: \

                               Value 0 = If this value is set, the function must receive at least \
                               one file name to be deleted. Can pass as many files as you want.

                               Value 1 = If this value is set, the function revokes the \
                               unitary file exclusion option, that is, this option will \
                               exclude all files at the root of the informed directory.

                               Value 2 = If this value is set, the function revokes the unitary \
                               file exclusion option as well, however, it will exclude all \
                               subdirectories of the root directory, except the files contained \
                               in the root.
    """

    data = next(walk(directory))

    #: DANGER!
    if level == 1:
        for f in data[2]:
            remove(join(data[0], f))
        return 1

    #: DANGER!
    if level == 2:
        # r: root, r: directory, f: files
        for r, d, f in walk(directory, topdown=False):
            for item in d:
                with ThreadPoolExecutor() as executor:
                    executor.submit(rmtree, join(r, item))
        return 2

    try:
        if file:
            for f in file:
                remove(join(data[0], f))
        return 0
    except FileNotFoundError as err:
        msg = ">>> There was an error removing the files"
        raise FileNotFoundError(msg, err)


__all__ = ["rmdir_blank", "remove_objects", "cleaner"]
