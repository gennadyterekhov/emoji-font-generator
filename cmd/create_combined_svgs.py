"""
create an SVG file for every word in dictionary.json
"""
from pathlib import Path

from emoji_font_generator.combine import  combine_wordform
from emoji_font_generator.input.config import get_dictionary
from emoji_font_generator.project import  get_project_dir


def main():
    root = get_project_dir()
    words = get_dictionary()
    prefix = f'{root}/emojis/combined'
    failures = 0
    for i, w in enumerate(words):
        natural_word = w.natural
        try:
            print(f'processing {w.conlang}={natural_word}, {i}/{len(words)}')
            if Path(f'{prefix}/{natural_word}.svg').exists():
                continue
            combine_wordform(w)
        except Exception as e:
            failures += 1
            print(e)
    print(f'total failures: {failures}')


if __name__ == "__main__":
    main()
