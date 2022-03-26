import pathlib
import sys
import json


def get_data_dir() -> pathlib.Path:
    """Get path to user data directory for current OS.

    Returns:
        pathlib.Path: path to user data directory
    """
    home = pathlib.Path.home()
    if sys.platform == "win32":
        return home / "AppData/Roaming"
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"


# Directory
def create_missing_dir(path) -> pathlib.Path:
    """"Creates specified directory if one doesn't exist

    Args:
        path (str | pathlib.Path): directory path

    Returns:
        pathlib.Path: Created directory.
    """
    path_obj = pathlib.Path(path) if not isinstance(path, pathlib.Path) else path
    if not path_obj.is_dir():
        path_obj.mkdir()

    return path_obj


# Json
def write_json(path: pathlib.Path, data: dict, as_string=False, sort_keys=True):
    """Write to json file.

    Args:
        path (pathlib.Path): path to json file
        data (dict): data to write
        as_string (bool, optional): if data should be writen as string. Defaults to False.
        sort_keys (bool, optional): if keys should be sorted. Defaults to True.
    """
    with path.open("w") as json_file:
        if as_string:
            json_file.write(json.dumps(data, sort_keys=sort_keys, indent=4, separators=(",", ":")))
        else:
            json.dump(data, json_file, indent=4)


def load_json(path: pathlib.Path, string_data=False) -> dict:
    """Loads data from given json file.

    Args:
        path (pathlib.Path): path to json file
        string_data (bool, optional): if data is written as string. Defaults to False.

    Returns:
        dict: loaded data
    """
    with path.open("r") as json_file:
        if string_data:
            data = json.loads(json_file)
        else:
            data = json.load(json_file)
    return data
