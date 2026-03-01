"""
this is a temporary script to add lirbantu words to ai_output.json so that we can use translated words for the font ligatures
"""
from emoji_font_generator.config.config import get_dictionary, get_wordform_index_from_ai_dictionary
from emoji_font_generator.project import read_json_file, get_project_dir, write_json_file


def enrich(before: list[dict]) -> list[dict]:
    after = []
    return after


def main():
    rootdir = get_project_dir()
    pth = f'{rootdir}/config/ai_output.json'
    raw_dict = read_json_file(f'{rootdir}/config/dict.json')
    before = get_dictionary()
    after = []
    for pair in raw_dict:
        lirbantu = pair[0].replace('\n', ',')
        russian = pair[1].replace('\n', ',')

        wf_index = get_wordform_index_from_ai_dictionary(russian)
        if wf_index is not None:
            before[wf_index]['lirbantu'] = lirbantu
    after=[]
    for wf in before:
        if 'lirbantu' in wf and  wf['lirbantu'] != '':
            after.append(wf)



    # after = enrich(before)
    write_json_file(f'{rootdir}/config/ai_output_w_lirbantu.json', after)


if __name__ == "__main__":
    main()
