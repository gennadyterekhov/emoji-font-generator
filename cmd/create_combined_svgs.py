"""
create an SVG file for every word in ai_output.json
"""
from pathlib import Path

from lirbantu.combine import combine4, combine_wordform
from lirbantu.project import read_json_file, get_project_dir


def main():
    root = get_project_dir()
    words = read_json_file(f"{root}/config/ai_output.json")
    prefix = f'{root}/emojis/combined'
    failures = 0
    for i, w in enumerate(words):
        try:
            print(f'processing {w["wordform"]}, {i}/{len(words)}')
            wordform = w["wordform"]
            if Path(f'{prefix}/{wordform}.svg').exists():
                continue
            combine_wordform(w)
        except Exception as e:
            failures += 1
            print(e)
    print(f'total failures: {failures}')


if __name__ == "__main__":
    main()
