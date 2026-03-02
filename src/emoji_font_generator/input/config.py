import dataclasses

from emoji_font_generator.input.io import read_json_file, write_json_file
from emoji_font_generator.project import get_project_dir
import os


@dataclasses.dataclass
class LlmConfig:
    api_key: str
    model_name: str
    base_url: str
    use_reasoning: bool = False


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", 'True', "yes", "y", "on"}


def get_llm_config_from_env() -> LlmConfig:
    api_key = os.getenv('LLM_API_KEY', '')
    model_name = os.getenv('LLM_MODEL_NAME', '')
    base_url = os.getenv('LLM_URL', '')
    use_reasoning = parse_bool(os.getenv('LLM_USE_REASONING', 'false'))
    return LlmConfig(api_key, model_name, base_url, use_reasoning)


def get_conlang_font_filename():
    root = get_project_dir()
    return f'{root}/input/fonts/input_font.ttf'


def get_config():
    root = get_project_dir()
    path = f'{root}/input/config/config.json'
    dct = read_json_file(path)
    return dct


def get_raw_sheet():
    root = get_project_dir()
    path = f'{root}/input/raw/sheet.json'
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


def save_new_dictionary(data: list[dict]) -> None:
    root = get_project_dir()
    path = f'{root}/input/config/dictionary.json'
    return write_json_file(path, data)


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
