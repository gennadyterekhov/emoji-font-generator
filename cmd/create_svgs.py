"""
create an SVG file for every word in ai_output.json
"""
from pathlib import Path

from lirbantu.combine import combine4
from lirbantu.project import read_json_file, get_project_dir


def main():
    root = get_project_dir()
    words=read_json_file(f"{root}/config/ai_output.json")
    failures=0
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
            failures+=1
            print(e)
    print(f'total failures: {failures}')


if __name__ == "__main__":
    main()