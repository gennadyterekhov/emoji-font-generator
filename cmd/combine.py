import xml.etree.ElementTree as ET

from lirbantu.project import get_project_dir

ET.register_namespace('', "http://www.w3.org/2000/svg")
ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")

root = ET.Element('{http://www.w3.org/2000/svg}svg', {
    'width': '400',
    'height': '400',
    'viewBox': '0 0 400 400',
    'version': '1.1',
    'xmlns': 'http://www.w3.org/2000/svg',
    'xmlns:xlink': 'http://www.w3.org/1999/xlink'
})

files = ['square1.svg', 'square2.svg', 'square3.svg', 'square4.svg']
prefix = get_project_dir()
files = [f'{prefix}/emojis/1f440.svg', f'{prefix}/emojis/1f441.svg', f'{prefix}/emojis/1f443.svg',
         f'{prefix}/emojis/1f444.svg']
x_offsets = [0, 200, 0, 200]
y_offsets = [0, 0, 200, 200]

for i, file in enumerate(files):
    tree = ET.parse(file)
    svg_root = tree.getroot()

    for element in svg_root:
        element.set('transform', f'translate({x_offsets[i]}, {y_offsets[i]})')
        root.append(element)

tree = ET.ElementTree(root)
tree.write(f'{prefix}/emojis/combined.xml', encoding='utf-8', xml_declaration=True)

import os

os.rename(f'{prefix}/emojis/combined.xml', f'{prefix}/emojis/combined.svg')
