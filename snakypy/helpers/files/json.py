import json
from os.path import exists, splitext


def read_json(file_path: str) -> dict:
    """
    Function that reads JSON configuration file and returns data.

    >>> from snakypy import helpers
    >>> file = '/tmp/file.json'
    >>> helpers.files.read_json(file)

    Args:
        file_path (str): You must receive the full/absolute file path

    Returns:
        [dict]: If the file is found it will return a dictionary
    """

    try:
        with open(file_path) as f:
            data = json.load(f)
        return data
    except FileNotFoundError as err:
        raise FileNotFoundError(f">>> File not found {err}")
    except json.decoder.JSONDecodeError:
        raise Exception(f">>> Incorrect Json file structure: {file_path}")
    except PermissionError:
        raise PermissionError(
            f"Your user does not have permission to read this file. {file_path}"
        )
    except Exception:
        raise Exception(f">>> There was an error reading the file: {file_path}")


def create_json(dictionary: dict, file_path: str, force: bool = False) -> bool:
    """
    Create a JSON file through a dictionary.

    >>> from snakypy import helpers
    >>> content = {"Hello": "World!"}
    >>> helpers.files.create_json(content, "/tmp/file.json", force=True)
    True

    Args:
        dictionary (dict): Must receive a dictionary

        file_path (str): You must receive the full/absolute file path.

        force (bool): Use the True option if you want to overwrite the existing file. (default: {False})

    Returns:
        [bool]: If everything went well, it will return True.
    """

    if splitext(file_path)[1] != ".json":
        raise Exception("The JSON file extension was not explicit.")
    if not force and exists(file_path):
        raise FileExistsError(
            f">>> The file {file_path} already exists, use force=True."
        )
    else:
        try:
            if type(dictionary) is dict:
                with open(file_path, "w") as f:
                    json.dump(dictionary, f, indent=4, separators=(",", ": "))
                    return True
            return False
        except PermissionError:
            raise PermissionError(
                f"Your user is not allowed to write to this file. {file_path}"
            )
        except Exception as err:
            raise Exception(f">>> There was an error creating the file. {err}")


def update_json(file_path: str, content: dict) -> bool:
    """
    Function to update json file. The "snakypy.json.read" function depends on
    reading a json file.

    >>> from snakypy import helpers
    >>> data = helpers.files.read_json('/tmp/file.json')
    >>> data['Hello'] = 'Olá, Snakypy!'
    >>> helpers.files.update_json('/tmp/file.json', data)
    True

    Args:
        file_path (str): You must receive the full/absolute file path.

        content (dict): You should receive a dictionary with the updated data already.

    Returns:
        [bool]: If everything went well, it will return True.
    """
    try:
        if type(content) is dict:
            with open(file_path, "w") as f:
                json.dump(content, f, indent=2, separators=(",", ": "))
            return True
        return False
    except PermissionError:
        raise PermissionError(
            f"Your user is not allowed to write to this file. {file_path}"
        )
    except Exception as err:
        msg = f">>> Something unexpected happened while updating {file_path}"
        raise Exception(msg, err)


__all__ = ["read_json", "create_json", "update_json"]
