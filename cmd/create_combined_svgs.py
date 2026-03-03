"""
create an SVG file for every word in dictionary.json
"""
from pathlib import Path

from emoji_font_generator.combine import combine_wordform
from emoji_font_generator.input.config import get_dictionary
from emoji_font_generator.project import get_project_dir


def main():
    root = get_project_dir()
    words = get_dictionary()
    prefix = f'{root}/input/emojis/combined'
    failures = 0
    skipped = 0
    for i, w in enumerate(words):
        natural_word = w.natural
        try:
            print(f'processing {w.conlang}={natural_word}, {i}/{len(words)}', end='')
            if Path(f'{prefix}/{natural_word}.svg').exists():
                print(f'👴')
                continue

            if w.root1_emoji and w.root2_emoji and w.grammar and w.logic:
                combine_wordform(w)
                print(f'✅')
                continue
            skipped += 1
            print(f'💩')
        except Exception as e:
            failures += 1
            print(f'❌')
            print(e)
    print(f'total failures: {failures}')
    print(f'total skipped: {skipped}')


if __name__ == "__main__":
    main()
