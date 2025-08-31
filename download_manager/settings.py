import json
import os

class Settings:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.default_settings = {
            "download_directory": os.path.join(os.path.expanduser("~"), "Downloads")
        }
        self.settings = self.load_settings()

    def load_settings(self):
        if not os.path.exists(self.filename):
            return self.default_settings
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self.default_settings

    def save_settings(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except IOError as e:
            print(f"Error saving settings: {e}")

    def get(self, key):
        return self.settings.get(key, self.default_settings.get(key))

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()
