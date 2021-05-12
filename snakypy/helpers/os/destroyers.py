from os import listdir, rmdir
from contextlib import suppress
from os.path import isdir
from concurrent.futures import ThreadPoolExecutor
from os import walk, remove
from os.path import join
from shutil import rmtree


def remove_objects(*, objects: tuple = ()) -> tuple:
    with suppress(FileNotFoundError):
        for item in objects:
            rmtree(item, ignore_errors=True) if isdir(item) else remove(item)
    return objects


def rmdir_blank(path: str) -> None:
    """
    Removes folders recursively if they are empty from a
    certain path.

    >>> import snakypy
    >>> snakypy.helpers.os.rmdir_blank("/tmp/program_x")

    or using from

    >>> from snakypy.helpers.os import rmdir_blank
    >>> rmdir_blank("/tmp/program_x")

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


def cleaner(directory, *file, level=-1) -> int:
    """
    **DANGER!** A function for cleaning objects and folders on the system.

    E.g:

    >>> import snakypy
    >>> snakypy.helpers.os.cleaner("/tmp/foo", level=0)
    >>> snakypy.helpers.os.cleaner("/tmp/foo", level=1)
    >>> snakypy.helpers.os.cleaner("/tmp/foo", "bar.txt")

    or using from

    >>> from snakypy.helpers.os import cleaner
    >>> cleaner("/tmp/foo", level=0)
    >>> cleaner("/tmp/foo", level=1)
    >>> cleaner("/tmp/foo", "bar.txt")

    Arguments:
        **directory {str}** -- Directory where are the files to be destroyed

        ***file** -- Enter an N file name number (Optional)

    Keyword Arguments:
        **level {int}** -- This option receives 3 values, they are: \

                           Value 0 = If this value is set, the function revokes the \
                           unitary file exclusion option, that is, this option will \
                           exclude all files at the root of the informed directory.

                           Value 1 = If this value is set, the function revokes the unitary \
                           file exclusion option as well, however, it will exclude all \
                           subdirectories of the root directory, except the files contained \
                           in the root.

                           Value None = If this value is set, the function must receive at least \
                           one file name to be deleted. Can pass as many files as you want.

                           (default: {None})

    """

    data = next(walk(directory))

    #: DANGER!
    if level == 0:
        for f in data[2]:
            remove(join(data[0], f))
        return 0

    #: DANGER!
    if level == 1:
        # r: root, r: directory, f: files
        for r, d, f in walk(directory, topdown=False):
            for item in d:
                with ThreadPoolExecutor() as executor:
                    executor.submit(rmtree, join(r, item))
        return 1

    try:
        if file:
            for f in file:
                remove(join(data[0], f))
        return -1
    except FileNotFoundError as err:
        msg = ">>> There was an error removing the files"
        raise FileNotFoundError(msg, err)


__all__ = ["rmdir_blank", "remove_objects", "cleaner"]
