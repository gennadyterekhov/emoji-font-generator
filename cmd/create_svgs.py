"""
create an SVG file for every word in ai_output.json
"""
from pathlib import Path

from lirbantu.combine import combine4
from lirbantu.project import read_json_file



def main():
    words=read_json_file(Path("ai_output.json"))

    for i,w in enumerate(words):
        try:
            print(f'processing {w["wordform"]}, {i}/{len(words)}')
            combine4(w['wordform'],[
                w['root1_emoji'],
                w['root2_emoji'],
                w['logic'],
                w['grammar'],
            ])
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()