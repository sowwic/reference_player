import pathlib
import dataclasses

from reference_player import Logger
from reference_player.utils import fileFn


CONFIG_FILE_PATH = fileFn.get_data_dir() / "reference_player" / "config.json"


@dataclasses.dataclass
class Config:
    window_size: tuple[int] = (600, 400)
    window_position: tuple[int] = tuple()
    window_always_on_top: bool = True
    logging_level: int = 10
    maya_port: int = 7221
    maya_autoconnect: bool = False

    @classmethod
    def get_fields_names(cls):
        """Get available config field names.

        Returns:
            set: set of existing field names
        """
        return set(each_field.name for each_field in dataclasses.fields(cls))

    @classmethod
    def _load_from_json(cls, file_path: pathlib.Path):
        """Create Config instance from given json file.

        Args:
            file_path (pathlib.Path): path to json file

        Returns:
            Config: new instance
        """
        json_data = fileFn.load_json(file_path)
        field_names = cls.get_fields_names()
        for json_field_name in list(json_data.keys()):
            if json_field_name not in field_names:
                json_data.pop(json_field_name)
                Logger.warning(f"Unused config field name: {json_field_name}")
        Logger.info(f"Loaded config: {CONFIG_FILE_PATH}")
        return cls(**json_data)

    @classmethod
    def reset(cls):
        """Write default config values to file.

        Returns:
            Config: default config instance
        """
        instance = cls()
        fileFn.create_missing_dir(CONFIG_FILE_PATH.parent)
        fileFn.write_json(CONFIG_FILE_PATH, dataclasses.asdict(instance))
        Logger.info("Config reset")
        return instance

    @classmethod
    def load(cls):
        """Load config from CONFIG_FILE_PATH

        Returns:
            Config: new instance
        """
        fileFn.create_missing_dir(CONFIG_FILE_PATH.parent)
        if not CONFIG_FILE_PATH.is_file():
            return cls.reset()
        return cls._load_from_json(CONFIG_FILE_PATH)

    def save(self):
        """Write config to json file."""
        fileFn.create_missing_dir(CONFIG_FILE_PATH.parent)
        fileFn.write_json(CONFIG_FILE_PATH, dataclasses.asdict(self))
        Logger.info(f"Saved config: {CONFIG_FILE_PATH}")
