from os import walk
from os.path import exists, isdir, join
from shutil import which

from snakypy.helpers.decorators import only_linux


def find_objects(
    directory: str, /, files: tuple = (), folders: tuple = (), by_extension: tuple = ()
) -> dict:
    """
    Find files, folders and files through its extensions.

    >>> from snakypy import helpers
    >>> helpers.catches.find_objects(".", files=("mypi.ini",), folders=("snakypy",), by_extension=("txt",))
    {'files': [], 'folders': [], 'by_extension': []}

    Args:
        directory (str): Enter the path of the root directory for the search

        files (tuple): You should receive a tuple and enter only the name of the file together with its extension

        folders (tuple): You should receive a tuple and enter only the name of the folder

        by_extension (tuple): You should receive a tuple and inform the extensions (without periods) of the files
                              you want to search for.

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
    """
        Searches if a tool is installed on the machine. (Linux systems only)

        >>> from snakypy import helpers
        >>> helpers.catches.is_tool("ls")
        True

    Args:
        args (str): You must enter the name of the application you want to search for. You can pass as many
                    parameters as you want, however, if you don't find one, the return will be False.

    Returns:
        [bool] -- Returns True if all are found or False if none or none are not found.
    """
    for tool in args:
        if which(tool) is not None:
            return True
    return False


@only_linux
def tools_requirements(*args) -> bool:
    """
        Search required tools if you can not burst an exception

        >>> from snakypy import helpers
        >>> helpers.catches.tools_requirements("ls", "cat", "chmod")
        True

    Args:
        args: You must receive the name of the tool to be searched on the machine. You can pass as many as you want.

    Returns:
        Returns true or an exception.
    """
    for tool in args:
        if which(tool) is None:
            raise FileNotFoundError(
                f'The tool "{tool}" is not installed on the operating system.'
            )
    return True


__all__ = ["find_objects", "is_tool", "tools_requirements"]
