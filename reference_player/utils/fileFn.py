import pathlib
import sys
import json
from reference_player import Logger


def get_data_dir() -> pathlib.Path:
    home = pathlib.Path.home()
    if sys.platform == "win32":
        return home / "AppData/Roaming"
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"


# Directory
def create_missing_dir(path, default_data="") -> pathlib.Path:
    """Creates specified directory if one doesn't exist

    :param path: Directory path
    :type path: str
    :return: Path to directory
    :rtype: pathlib.Path
    """
    path_obj = pathlib.Path(path)
    if not path_obj.is_dir():
        path_obj.mkdir()

    return path_obj


# Json
def write_json(path, data={}, as_string=False, sort_keys=True):
    try:
        with open(path, "w") as json_file:
            if as_string:
                json_file.write(json.dumps(data, sort_keys=sort_keys, indent=4, separators=(",", ":")))
            else:
                json.dump(data, json_file, indent=4)

    except IOError as e:
        Logger.exception("{0} is not a valid file path".format(path), exc_info=e)
        return None

    except BaseException:
        Logger.exception("Failed to write file {0}".format(path), exc_info=1)
        return None

    return path


def load_json(path, string_data=False):
    try:
        with open(path, "r") as json_file:
            if string_data:
                data = json.loads(json_file)
            else:
                data = json.load(json_file)

    except IOError:
        Logger.exception("{0} is not a valid file path".format(path))
        return None
    except BaseException:
        Logger.exception("Failed to load file {0}".format(path))
        return None

    return data  # type:dict
