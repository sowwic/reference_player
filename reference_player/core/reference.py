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
        self.data: dict = data
        self.signals = ReferenceSignals()
        Logger.debug(self)

    @property
    def path(self):
        return self.media_file.with_suffix(self.FILE_EXTENSION)

    def save(self):
        fileFn.write_json(self.path, self.data)

    def is_media_file_valid(self):
        return self.media_file.is_file()

    @property
    def media_file(self) -> pathlib.Path:
        return pathlib.Path(self.data.get("media_file"))

    @media_file.setter
    def media_file(self, file_path: pathlib.Path):
        self.data["media_file"] = file_path.as_posix()
        self.signals.media_file_changed.emit(file_path)

    @property
    def name(self):
        return self.data.get("name", self.path.stem)

    @classmethod
    def from_file(cls, file_path: pathlib.Path):
        instance: Reference = None
        if file_path.suffix == cls.FILE_EXTENSION:
            reference_data = fileFn.load_json(file_path)
            instance = cls(reference_data)
        else:
            reference_data = {"media_file": file_path.as_posix(),
                              "name": file_path.name}
            instance = cls(reference_data)
            instance.save()

        return instance
