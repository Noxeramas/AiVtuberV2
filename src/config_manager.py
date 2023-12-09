import json


class ConfigManager:
    def __init__(self, config_file_path):
        self.settings = self.load_settings(config_file_path)


def load_settings(file_path):
    """
    :param file_path:
    :return:

    Loads settings from a file.
    """

    with open(file_path, 'r') as f:
        return json.load(f)
