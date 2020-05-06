import os
import json

class Settings:
    def __init__(self):
        self.defaults = {"port" : 7221}
        self.directory = os.path.join(os.getenv("LOCALAPPDATA"), "dsReferencePlayer")
        self.fileName = "settings.json"
        self.filePath = os.path.join(self.directory, self.fileName)
        
        # Settings
        self.port = 7221
        
        # Create default settings if missing
        self._createMissingSettings()
        
    def save(self, defaults=False):       
        current = {"port" : self.port}
        with open(self.filePath, "w") as jsonFile:
            if defaults:
                saveData = json.dump(self.defaults, jsonFile, indent=4)
                return
         
            saveData = json.dump(current, jsonFile, indent=4)
            
    def load(self):
        self._createMissingSettings()
        with open(self.filePath, "r") as jsonFile:
            data = json.load(jsonFile)
        
        self.port = data["port"]

        return data
        
    def _createMissingSettings(self):
        # Directory
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)
        # Default settings file
        if not os.path.isfile(self.filePath):
            self.save(defaults=True)