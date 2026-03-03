from emoji_font_generator.input.config import get_conlang_font_filename
from emoji_font_generator.ligature import get_ligatures_map, add_svg_ligatures_to_font
from emoji_font_generator.project import get_project_dir


def main():
    rootdir = get_project_dir()
    output_filename = f'{rootdir}/output/fonts/output_font.ttf'
    ligatures = get_ligatures_map()
    add_svg_ligatures_to_font(get_conlang_font_filename(), ligatures, output_filename)


if __name__ == '__main__':
    main()
