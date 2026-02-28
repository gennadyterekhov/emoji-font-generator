from pathlib import Path

from lirbantu.project import get_project_dir


def get_emoji_svg_path(emoji_char: str) -> str:
    codepoint = format(ord(emoji_char), 'x')
    root = get_project_dir()
    return f'{root}/emojis/twemoji/{codepoint}.svg'


def get_emoji_svg_path_or_throw(emoji_char: str) -> str:
    codepoint = format(ord(emoji_char), 'x')
    root = get_project_dir()
    path = f'{root}/emojis/twemoji/{codepoint}.svg'
    if Path(path).exists():
        return path
    raise Exception(f'Could not find svg {path}')
