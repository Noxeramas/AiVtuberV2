import json
import os
from data import constants
import config_paths

config_file_path = config_paths.get_config_file_path()


class BaseRequestManager:
    def __init__(self, config_file=config_file_path):
        with open(config_file, 'r') as f:
            self.json_data = json.load(f)
        self.request = {}

    def set(self, key, value):
        if key in self.request:
            self.request[key] = value
        else:
            raise KeyError(f"Key {key} not in request")

    def build(self):
        return self.request

    def save_to_file(self, config_file=config_file_path):
        with open(config_file, 'w') as f:
            json.dump(self.json_data, f, indent=4)


class OobaboogaRequestManager(BaseRequestManager):
    def __init__(self, config_file=config_file_path):
        super().__init__(config_file)
        self.request = self.json_data['ooba_request']


class StableDiffusionRequestManager(BaseRequestManager):
    def __init__(self, config_file=config_file_path):
        super().__init__(config_file)
        self.request = self.json_data['stable_diffusion_request']
        if self.request['prompt'] == '':
            self.request['prompt'] = constants.PROMPT
            self.request['negative_prompt'] = constants.NEGATIVE_PROMPT
            self.json_data['stable_diffusion_request'] = self.request
            self.save_to_file(config_file)


class ElevenlabRequestManager(BaseRequestManager):
    def __init__(self, config_file=config_file_path):
        super().__init__(config_file)
        self.request = self.json_data['elevenlab_data']


class CharacterAiRequestManager(BaseRequestManager):
    def __init__(self, config_file=config_file_path):
        super().__init__(config_file)
        self.request = self.json_data['character_ai_data']


class OpenAiRequestManager(BaseRequestManager):
    def __init__(self, config_file=config_file_path):
        super().__init__(config_file)
        self.request = self.json_data['openai_data']
