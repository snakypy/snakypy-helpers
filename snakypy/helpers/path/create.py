from pathlib import Path


def create(*args: str) -> None:
    """
    Function that creates single or multiple directories.

    >>> from snakypy.helpers.path import create
    >>> dirs = ("/tmp/foo/bar", "/tmp/foo/xyz")
    >>> create("/tmp/bar", "/tmp/bar/foo")
    >>> create(*dirs)

    Arguments:
        args (str): You must receive one or more unique arguments.
    """
    try:
        # Create directory single.
        if args:
            for directory in args:
                path = Path(directory)
                path.mkdir(parents=True, exist_ok=True)
    except TypeError:
        raise TypeError(
            ">>> Invalid type. You should receive only one argument at a time."
        )
    except Exception:
        raise Exception(f">>> An error occurred while creating directory: {args}")
