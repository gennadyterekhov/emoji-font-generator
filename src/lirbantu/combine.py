import xml.etree.ElementTree as ET

from lirbantu.helpers import get_emoji_svg_path_or_throw, get_logic_svg_path_or_throw, get_grammar_svg_path_or_throw
from lirbantu.project import get_project_dir
import os


def combine4(wordform: str, emojis: list[str]):
    if len(emojis) != 4:
        raise ValueError('Emojis must have exactly 4 characters')
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

    prefix = get_project_dir()
    pic1 = get_emoji_svg_path_or_throw(emojis[0])
    pic2 = get_emoji_svg_path_or_throw(emojis[1])
    logic = get_logic_svg_path_or_throw(emojis[2])
    grammar = get_grammar_svg_path_or_throw(emojis[3])
    paths = [pic1, pic2, logic, grammar]
    fname = '_'.join(emojis)

    x_offsets = [0, 200, 0, 200]
    y_offsets = [0, 0, 200, 200]

    for i, file in enumerate(paths):
        tree = ET.parse(file)
        svg_root = tree.getroot()

        for element in svg_root:
            translate = f'translate({x_offsets[i]}, {y_offsets[i]})'
            scale = f'scale(5, 5)'
            if i < 2:
                element.set('transform', f'{translate} {scale}')
            else:
                element.set('transform', f'{translate}')
            root.append(element)

    tree = ET.ElementTree(root)
    tree.write(f'{prefix}/emojis/combined/temp.xml', encoding='utf-8', xml_declaration=True)

    os.rename(f'{prefix}/emojis/combined/temp.xml', f'{prefix}/emojis/combined/{wordform}.svg')
