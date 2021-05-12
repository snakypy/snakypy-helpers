from shutil import which
from os.path import isdir, join, exists
from os import walk
from snakypy.helpers.utils.decorators import only_linux


def find_objects(
    directory: str, /, files: tuple = (), folders: tuple = (), by_extension: tuple = ()
) -> dict:
    """Find files, folders and files through its extensions.

    >>> import snakypy
    >>> snakypy.helpers.catches.find_objects("/tmp", files=("file.txt",), folders=("snakypy",), by_extension=("txt",))

    or using from

    >>> from snakypy.helpers.catches import find_objects
    >>> find_objects("/tmp", files=("file.txt",), folders=("snakypy",), by_extension=("py",))

    **output:**

    .. code-block:: shell

        {'files': ['/tmp/file.txt', '/tmp/foo.txt'], 'folders': ['/tmp/snakypy'],
        'extension': ['/tmp/snakypy.py', '/tmp/bar.py']}

    Arguments:
        **directory {str}** -- Enter the path of the root directory for the search

        **files {tuple}** -- You should receive a tuple and enter only the name of the
                             file together with its extension

        **folders {tuple}** -- You should receive a tuple and enter only the name of the folder

        **by_extension {tuple}** -- You should receive a tuple and inform the extensions
                                    (without periods) of the files you want to search for.

    Returns:
        [dict] -- It will return a dictionary with the following structure:
                  {'files': [], 'folders': [], 'extension': []}
    """

    # Create base data
    data: dict = {"files": [], "folders": [], "by_extension": []}

    try:

        if files:
            for file in files:
                if exists(join(directory, file)):
                    data["files"].append(join(directory, file))

        if by_extension:
            for ext in by_extension:
                for root_, directory_, files_ in walk(directory):
                    for file in files_:
                        if file.endswith(ext):
                            data["by_extension"].append(join(root_, file))

        if folders:
            for folder in folders:
                if isdir(join(directory, folder)):
                    data["folders"].append(join(directory, folder))

        return data

    except PermissionError:
        raise PermissionError(
            "Your user is not allowed to scan that directory. Aborted"
        )


@only_linux
def is_tool(*args: str) -> bool:
    """Searches if a tool is installed on the machine. (Linux systems only)

    >>> import snakypy
    >>> snakypy.helpers.catches.is_tool("ls")

    or using from

    >>> from snakypy.helpers.catches import is_tool
    >>> is_tool("ls")

    **output:**

    .. code-block:: shell

        True

    Arguments:
        **args {str}** -- You must enter the name of the application you want to search for.
                          You can pass as many parameters as you want, however, if you don't
                          find one, the return will be False.

    Returns:
        [bool] -- Returns True if all are found or False if none or none are not found.
    """
    for tool in args:
        if which(tool) is not None:
            return True
    return False


@only_linux
def tools_requirements(*args) -> bool:
    for tool in args:
        if which(tool) is None:
            raise FileNotFoundError(
                f'The tool "{tool}" is not installed on the operating system.'
            )
    return True


__all__ = ["find_objects", "is_tool", "tools_requirements"]
