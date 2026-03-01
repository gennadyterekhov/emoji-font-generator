from pathlib import Path

from lirbantu.project import get_project_dir


def get_emoji_svg_path(emoji_char: str) -> str:
    codepoint = get_twemoji_codepoint(emoji_char)
    root = get_project_dir()
    return f'{root}/emojis/twemoji/{codepoint}.svg'


def get_emoji_svg_path_or_throw(emoji_char: str) -> str:
    root = get_project_dir()
    codepoint = get_twemoji_codepoint(emoji_char)
    path = f'{root}/emojis/twemoji/{codepoint}.svg'
    if Path(path).exists():
        return path
    raise Exception(f'Could not find svg for {emoji_char} in {path}')


def get_grammar_svg_path_or_throw(grammar: str) -> str:
    root = get_project_dir()
    path = f'{root}/emojis/grammar/{grammar}.svg'
    if Path(path).exists():
        return path
    raise Exception(f'Could not find svg for {grammar} in {path}')


def get_logic_svg_path_or_throw(logic: str) -> str:
    root = get_project_dir()
    path = f'{root}/emojis/logic/{logic}.svg'
    if Path(path).exists():
        return path
    raise Exception(f'Could not find svg for {logic} in {path}')


def get_twemoji_codepoint(emoji_char, ):
    total = ''
    for char in emoji_char:
        codepoint = format(ord(char), 'x')
        total += f'-' + codepoint
    return total[1:]
