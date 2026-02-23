from lirbantu.project import get_project_dir, read_json_file


def get_config():
    root = get_project_dir()
    path = f'{root}/config/config.json'
    dct = read_json_file(path)
    return dct


def get_system() -> list:
    root = get_project_dir()
    path = f'{root}/config/system.json'
    dct = read_json_file(path)
    return dct


def get_usable_emojis() -> list:
    root = get_project_dir()
    path = f'{root}/config/usable_emojis.json'
    dct = read_json_file(path)
    return dct
