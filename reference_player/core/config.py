import shutil
import pathlib
from reference_player import Logger
from reference_player.utils import fileFn


class Config:

    DEFAULT_CONFIG_FILE = pathlib.Path.cwd() / "default_config.json"
    APP_DIR = fileFn.get_data_dir() / "reference_player"

    @classmethod
    def load(cls):
        """Load config as dict

        Returns:
            dict: Config dictionary
        """
        return fileFn.load_json(cls.get_config_file())

    @classmethod
    def update(cls, new_config_dict):
        current_config = cls.load()  # type: dict
        current_config.update(new_config_dict)
        fileFn.write_json(cls.get_config_file(), current_config, sort_keys=True)

    @classmethod
    def get(cls, key, default=None):
        """Get setting by key

        Args:
            key (str): Setting name
            default (any, optional): Default value to set if key doesn't exist. Defaults to None.

        Returns:
            any: Value for requested setting
        """
        current_config = cls.load()  # type:dict
        if key not in current_config.keys():
            current_config[key] = default
            cls.update(current_config)
        return current_config.get(key)

    @classmethod
    def set(cls, key, value):
        """Sets setting to passed value

        Args:
            key (str): Setting name
            value (any): Value to set
        """
        cls.update({key: value})

    @classmethod
    def reset(cls):
        """
        Reset config to default. Copies default config file with normal config name
        """
        file_path = Config.APP_DIR / "config.json"
        fileFn.create_missing_dir(Config.APP_DIR)
        shutil.copy2(Config.DEFAULT_CONFIG_FILE, file_path)
        Logger.info("Config reset to default")

    @ staticmethod
    def get_config_file():
        """Get path to config file. Copy a default one if one doesn't exist.

        Returns:
            str: Path to config file
        """
        file_path = Config.APP_DIR / "config.json"
        fileFn.create_missing_dir(Config.APP_DIR)
        if not file_path.is_file():
            shutil.copy(Config.DEFAULT_CONFIG_FILE, file_path)
            Logger.debug("Default config copied to: {0}".format(file_path))

        return file_path


if __name__ == "__main__":
    Config.reset()
