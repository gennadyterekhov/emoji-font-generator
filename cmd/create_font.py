import sys

from fontTools.ttLib import TTFont, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.misc.transform import Transform

from lirbantu.config.config import get_ai_dictionary


# import svg2ttf  # сторонняя библиотека для конвертации SVG в TTF

def create_ttf_from_svg(svg_map, output_path='output.ttf'):
    font = TTFont()

    # Базовые таблицы
    font['head'] = newTable('head')
    font['hhea'] = newTable('hhea')
    font['maxp'] = newTable('maxp')
    font['name'] = newTable('name')
    font['cmap'] = newTable('cmap')
    font['glyf'] = newTable('glyf')
    font['hmtx'] = newTable('hmtx')

    # Настройка базовых параметров
    font['head'].unitsPerEm = 1000
    font['maxp'].numGlyphs = len(svg_map) + 1  # +1 для .notdef

    glyphs = {}
    hmtx = {}

    # .notdef глиф
    pen = TTGlyphPen(None)
    glyphs['.notdef'] = pen.glyph()
    hmtx['.notdef'] = (600, 0)

    # Обработка SVG
    for char_code, svg_path in svg_map.items():
        glyph_name = f'uni{char_code:04X}'

        # Конвертация SVG (упрощённо)
        svg_font = svg2ttf.convert(svg_path)
        glyph = svg_font['glyf'][list(svg_font['glyf'].keys())[0]]

        glyphs[glyph_name] = glyph
        hmtx[glyph_name] = (600, 0)  # Нужно вычислять реально

    font['glyf'].glyphs = glyphs
    font['hmtx'].metrics = hmtx

    # cmap таблица
    cmap_table = newTable('cmap')
    cmap_table.tableVersion = 0
    cmap_table.tables = []

    from fontTools.ttLib.tables._c_m_a_p import cmap_format_4
    subtable = cmap_format_4(4)
    subtable.platformID = 3
    subtable.platEncID = 1
    subtable.language = 0
    subtable.cmap = {code: f'uni{code:04X}' for code in svg_map.keys()}

    cmap_table.tables.append(subtable)
    font['cmap'] = cmap_table

    font.save(output_path)


def get_svg_map():
    words=get_ai_dictionary()
    return {}


def main():
    svg_map = get_svg_map()
    create_ttf_from_svg(svg_map)


if __name__ == '__main__':
    main()
