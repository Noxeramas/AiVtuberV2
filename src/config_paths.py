import os


def get_parent_dir_of_current_script():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(current_dir)


def get_data_dir():
    parent_dir = get_parent_dir_of_current_script()
    return os.path.join(parent_dir, 'data')


def get_config_file_path():
    data_dir = get_data_dir()
    return os.path.join(data_dir, 'config.json')


def get_request_config_file_path():
    data_dir = get_data_dir()
    return os.path.join(data_dir, 'request_config.json')


def get_bot1_lore_file_path():
    data_dir = get_data_dir()
    return os.path.join(data_dir, 'bot1_openai_lore.txt')


def get_bot2_lore_file_path():
    data_dir = get_data_dir()
    return os.path.join(data_dir, 'bot2_openai_lore.txt')
