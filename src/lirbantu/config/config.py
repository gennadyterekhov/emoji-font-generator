from typing import Any

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


def get_ai_dictionary() -> list:
    root = get_project_dir()
    path = f'{root}/config/ai_output.json'
    return read_json_file(path)


def get_emojis_used_by_ai() -> list:
    words = get_ai_dictionary()
    emojis = [w['root1_emoji'] for w in words]
    emojis2 = [w['root2_emoji'] for w in words]
    emojis.extend(emojis2)
    emojis = list(set(emojis))
    return emojis


def get_wordform_from_ai_dictionary(wordform: str) -> dict | None:
    words = get_ai_dictionary()

    for w in words:
        if w['wordform'] == wordform:
            return w
    return None
