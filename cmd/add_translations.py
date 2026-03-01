"""
this is a temporary script to add lirbantu words to ai_output.json so that we can use translated words for the font ligatures
"""
from lirbantu.project import read_json_file, get_project_dir, write_json_file


def enrich(before, ):
    after = {}
    return after


def main():
    rootdir = get_project_dir()
    pth = f'{rootdir}/config/ai_output.json'
    before = read_json_file(pth)
    after = enrich(before)
    write_json_file(pth, after)


if __name__ == "__main__":
    main()
