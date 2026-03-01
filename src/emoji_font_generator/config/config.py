from emoji_font_generator.io import read_json_file
from emoji_font_generator.project import get_project_dir


def get_lirbantu_font_filename():
    root = get_project_dir()
    return f'{root}/input/fonts/input_font.ttf'


def get_config():
    root = get_project_dir()
    path = f'{root}/input/config/config.json'
    dct = read_json_file(path)
    return dct


def get_system() -> list:
    root = get_project_dir()
    path = f'{root}/input/config/system.json'
    dct = read_json_file(path)
    return dct

def get_dictionary() -> list[dict]:
    root = get_project_dir()
    path = f'{root}/input/config/dictionary.json'
    return read_json_file(path)


def get_emojis_used_by_ai() -> list:
    words = get_dictionary()
    emojis = [w['root1_emoji'] for w in words]
    emojis2 = [w['root2_emoji'] for w in words]
    emojis.extend(emojis2)
    emojis = list(set(emojis))
    return emojis


def get_wordform_from_ai_dictionary(wordform: str) -> dict | None:
    words = get_dictionary()
    for w in words:
        if w['wordform'] == wordform:
            return w
    return None


def get_wordform_index_from_ai_dictionary(wordform: str) -> int | None:
    words = get_dictionary()
    for i, w in enumerate(words):
        if w['wordform'] == wordform:
            return i
    return None
