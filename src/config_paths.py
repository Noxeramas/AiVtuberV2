import os


def get_parent_dir_of_current_script():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(current_dir)


def get_data_dir():
    parent_dir = get_parent_dir_of_current_script()
    return os.path.join(parent_dir, 'data')


def get_settings_file_path():
    data_dir = get_data_dir()
    return os.path.join(data_dir, 'settings.json')


def get_config_file_path():
    data_dir = get_data_dir()
    return os.path.join(data_dir, 'request_config.json')
