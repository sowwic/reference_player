import pathlib
from PySide2 import QtCore
from PySide2 import QtWidgets


from reference_player import Logger
from reference_player.utils import fileFn


class ReferenceSignals(QtCore.QObject):
    media_file_changed = QtCore.Signal(pathlib.Path)


class Reference:
    FILE_EXTENSION: str = ".vref"

    def __repr__(self) -> str:
        return f"Reference: {self.data}"

    def __init__(self, data: dict) -> None:
        self.path: pathlib.Path = None
        self.data: dict = data
        self.signals = ReferenceSignals()
        Logger.debug(self)

    def save(self, file_path: pathlib.Path):
        fileFn.write_json(file_path, self.data)
        self.path = file_path

    def is_media_file_valid(self):
        return self.media_file.is_file()

    @property
    def media_file(self) -> pathlib.Path:
        return pathlib.Path(self.data.get("media_file", "Null path"))

    @media_file.setter
    def media_file(self, file_path: pathlib.Path):
        self.data["media_file"] = file_path.as_posix()
        self.signals.media_file_changed.emit(file_path)

    @property
    def name(self):
        return self.data.get("name", "New reference")

    @name.setter
    def name(self, value: str):
        self.data["name"] = value

    @classmethod
    def from_file(cls, file_path: pathlib.Path):
        instance: Reference = None
        if file_path.suffix == cls.FILE_EXTENSION:
            reference_data = fileFn.load_json(file_path)
            instance = cls(reference_data)
            instance.path = file_path
        else:
            reference_data = {"media_file": file_path.as_posix(),
                              "name": file_path.name}
            instance = cls(reference_data)
            instance.save(file_path.with_suffix(cls.FILE_EXTENSION))

        return instance
