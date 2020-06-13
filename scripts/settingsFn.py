import os
import json


class Settings:
    DEFAULTS = {"port": 7221,
                "alwaysOnTop": True,
                "connectOnStart": False}

    def __init__(self):
        self.directory = os.path.join(os.getenv("LOCALAPPDATA"), "dsReferencePlayer")
        self.fileName = "settings.json"
        self.filePath = os.path.join(self.directory, self.fileName)
        self.current = self.DEFAULTS
        # Create default settings if missing
        self._createMissingSettings()

        # Load saved
        self.load()

    def save(self, defaults: bool = False):
        with open(self.filePath, "w") as jsonFile:
            if defaults:
                saveData = json.dump(self.DEFAULTS, jsonFile, indent=4)
            else:
                saveData = json.dump(self.current, jsonFile, indent=4)

        return saveData

    def load(self):
        self._createMissingSettings()
        with open(self.filePath, "r") as jsonFile:
            self.current = json.load(jsonFile)

    def _createMissingSettings(self):
        # Directory
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)
        # Default settings file
        if not os.path.isfile(self.filePath):
            self.save(defaults=True)
