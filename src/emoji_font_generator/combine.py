import xml.etree.ElementTree as ET

from emoji_font_generator.helpers import get_emoji_svg_path_or_throw, get_logic_svg_path_or_throw, \
    get_grammar_svg_path_or_throw
from emoji_font_generator.project import get_project_dir
import os

from emoji_font_generator.word import Word


def combine_wordform(word: Word | dict):
    if type(word) is Word:
        logic = word.logic
        grammar = word.grammar
        description = word.description
    else:
        logic = word.get("logic", 'genitive')
        grammar = word.get("grammar", 'noun')
        description = word.get('description', '')

    if logic == 'genitive' and grammar == 'noun':
        return combine2(word.conlang, [word.root1_emoji, word.root2_emoji, ], description, grammar)

    if logic == 'accusative' and grammar == 'infinitive':
        return combine3(word.conlang, [word.root1_emoji, word.root2_emoji, logic], description, grammar)

    return combine4(
        word.conlang,
        [
            word.root1_emoji,
            word.root2_emoji,
            logic,
            grammar,
        ],
        description,
        grammar
    )


def combine4(wordform: str, emojis: list[str], description='', grammar: str = ''):
    if len(emojis) != 4:
        raise ValueError('Emojis must have exactly 4 characters')
    root = get_svg_root(description)

    pic1 = get_emoji_svg_path_or_throw(emojis[0])
    pic2 = get_emoji_svg_path_or_throw(emojis[1])
    logic = get_logic_svg_path_or_throw(emojis[2])
    grammar = get_grammar_svg_path_or_throw(emojis[3])
    paths = [pic1, pic2, logic, grammar]
    fname = '_'.join(emojis)
    center_offset = 75
    x_offsets = [0, 200, 0 + center_offset, 200 + center_offset]
    y_offsets = [0, 0, 200 + center_offset, 200 + center_offset]

    for i, file in enumerate(paths):
        tree = ET.parse(file)
        svg_root = tree.getroot()

        for element in svg_root:
            translate = f'translate({x_offsets[i]}, {y_offsets[i]})'
            scale = f'scale(5, 8)'
            if i < 2:
                element.set('transform', f'{translate} {scale}')
            else:
                element.set('transform', f'{translate}')
            root.append(element)
    save_as_file(root, wordform, grammar)


def combine3(wordform: str, emojis: list[str], description='', grammar: str = ''):
    if len(emojis) != 3:
        raise ValueError('Emojis must have exactly 3 characters')
    root = get_svg_root(description)

    pic1 = get_emoji_svg_path_or_throw(emojis[0])
    pic2 = get_emoji_svg_path_or_throw(emojis[1])
    logic = get_logic_svg_path_or_throw(emojis[2])

    paths = [pic1, pic2, logic]
    fname = '_'.join(emojis)
    center_offset = 75
    x_offsets = [0, 200, 200, ]
    y_offsets = [0, 0, 200 + center_offset, ]

    for i, file in enumerate(paths):
        tree = ET.parse(file)
        svg_root = tree.getroot()

        for element in svg_root:
            translate = f'translate({x_offsets[i]}, {y_offsets[i]})'
            scale = f'scale(5, 8)'
            if i < 2:
                element.set('transform', f'{translate} {scale}')
            else:
                element.set('transform', f'{translate}')
            root.append(element)
    save_as_file(root, wordform, grammar)


def combine2(wordform: str, emojis: list[str], description='', grammar: str = ''):
    if len(emojis) != 2:
        raise ValueError('Emojis must have exactly 2 characters')
    root = get_svg_root(description)

    pic1 = get_emoji_svg_path_or_throw(emojis[0])
    pic2 = get_emoji_svg_path_or_throw(emojis[1])

    paths = [pic1, pic2]
    x_offsets = [0, 200]
    y_offsets = [0, 0]

    for i, file in enumerate(paths):
        tree = ET.parse(file)
        svg_root = tree.getroot()

        for element in svg_root:
            translate = f'translate({x_offsets[i]}, {y_offsets[i]})'
            scale = f'scale(5, 10)'
            element.set('transform', f'{translate} {scale}')
            root.append(element)

    save_as_file(root, wordform, grammar)


def save_as_file(root: ET.Element, wordform: str, grammar: str = ''):
    """ we need grammar to differentiate hieroglyphs of homograph forms like "коня" рд.п. и вин.п. """
    prefix = get_project_dir()
    tree = ET.ElementTree(root)
    tree.write(f'{prefix}/input/emojis/combined/temp.xml', encoding='utf-8', xml_declaration=True)
    if grammar:
        os.rename(f'{prefix}/input/emojis/combined/temp.xml',
                  f'{prefix}/input/emojis/combined/{wordform}_{grammar}.svg')
    else:
        os.rename(f'{prefix}/input/emojis/combined/temp.xml', f'{prefix}/input/emojis/combined/{wordform}.svg')


def get_svg_root(description='') -> ET.Element:
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")

    root = ET.Element('{http://www.w3.org/2000/svg}svg', {
        'width': '400',
        'height': '400',
        'viewBox': '0 0 400 400',
        'version': '1.1',
        # 'xmlns': 'http://www.w3.org/2000/svg',
        # 'xmlns:xlink': 'http://www.w3.org/1999/xlink'
    })
    comment = ET.Comment(f'description: {description} ')
    root.append(comment)
    return root
