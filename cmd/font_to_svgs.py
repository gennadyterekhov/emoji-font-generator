import os

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

from emoji_font_generator import project


def export_all_glyphs_to_svg(font_path, output_folder="glyphs_output"):
    """
    Экспортирует ВСЕ глифы из шрифта (включая иероглифы) в SVG.
    """
    # 1. Загружаем шрифт
    font = TTFont(font_path)
    os.makedirs(output_folder, exist_ok=True)

    # 2. Получаем таблицу соответствия "Unicode -> Имя глифа"
    cmap = font.getBestCmap()

    if not cmap:
        print("В шрифте не найдена Unicode-таблица!")
        return

    # 3. Подготавливаем объект для рисования контуров
    glyph_set = font.getGlyphSet()

    print(f"Найдено глифов в таблице: {len(cmap)}")
    print("Начинаю экспорт...")

    for unicode_int, glyph_name in cmap.items():
        # Пропускаем управляющие символы
        if unicode_int < 32:
            continue

        try:
            # Получаем объект глифа
            glyph = glyph_set[glyph_name]

            # --- Получаем SVG-путь ---
            svg_pen = SVGPathPen(glyph_set)
            glyph.draw(svg_pen)
            svg_path_data = svg_pen.getCommands()

            if not svg_path_data:
                continue

            # --- Получаем границы глифа (исправленная часть) ---
            bounds_pen = BoundsPen(glyph_set)
            glyph.draw(bounds_pen)
            bounds = bounds_pen.bounds

            if bounds:
                x_min, y_min, x_max, y_max = bounds
                width = x_max - x_min
                height = y_max - y_min
                viewbox = f"{x_min} {y_min} {width} {height}"
            else:
                # Fallback: если границы не вычислены
                viewbox = "0 0 1000 1000"

            # --- Формируем SVG (с переворотом кверх ногами) ---
            flip_transform = f"translate(0, {2 * y_min + height}) scale(1, -1)" if bounds else "scale(1, -1)"
            svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}">
  <g transform="{flip_transform}">
    <path fill="black" d="{svg_path_data}" />
  </g>
</svg>'''

            # --- Сохраняем файл ---
            safe_char = ''
            try:
                char = chr(unicode_int)
                safe_char = ''.join(c for c in char if c.isprintable() and c not in r'\/:*?"<>|')
            except:
                pass

            if safe_char:
                filename = f"{safe_char}_{unicode_int:04X}.svg"
            else:
                filename = f"glyph_{unicode_int:04X}.svg"

            filepath = os.path.join(output_folder, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(svg_content)

            if len(os.listdir(output_folder)) % 100 == 0:
                print(f"Обработано {len(os.listdir(output_folder))} глифов...")

        except Exception as e:
            print(f"Не удалось обработать {glyph_name} (U+{unicode_int:04X}): {e}")

    print(f"Готово! Файлы сохранены в папку: {output_folder}")


def main():

    pd = project.get_project_dir()
    font_path = f"{pd}/input/fonts/NotoSansEgyptianHieroglyphs-Regular.ttf"  # Укажите путь к вашему TTF или OTF файлу
    export_all_glyphs_to_svg(font_path, f"{pd}/input/egyptian")

    font_path = f"{pd}/input/fonts/NotoSansCuneiform-Regular.ttf"  # Укажите путь к вашему TTF или OTF файлу
    export_all_glyphs_to_svg(font_path, f"{pd}/input/cuneiform")


if __name__ == "__main__":
    main()
