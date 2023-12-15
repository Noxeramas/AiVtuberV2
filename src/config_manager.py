import json
import config_paths

config_path = config_paths.get_config_file_path()


class ConfigManager:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.load_settings()

    def load_settings(self):
        with open(self.config_file_path, 'r') as f:
            self.settings = json.load(f)
            self.twitch_username = self.settings['streaming_platforms']['twitch']['username']
            self.twitch_token = self.settings['streaming_platforms']['twitch']['token']
            self.openai_api_key = self.settings['streaming_platforms']['openai']['api_key']

    def save_settings(self):
        with open(self.config_file_path, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get_setting(self, keys, default=None):
        """
        Get a nested setting value using a list of keys.
        """
        value = self.settings
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set_setting(self, keys, value):
        """
        Set a nested setting value using a list of keys.
        """
        setting = self.settings
        for key in keys[:-1]:
            if key not in setting:
                setting[key] = {}
            setting = setting[key]
        setting[keys[-1]] = value
        self.save_settings()
