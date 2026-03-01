from emoji_font_generator.input.config import get_raw_sheet, save_new_dictionary


def sheet_to_dictionary(sheet: list[list]) -> list[dict]:
    columns = [
        "phaaga",
        "translations",
        "pos",
        "spheres",
        "etymology",
        "comment"
    ]
    dictionary = []
    for row in sheet:
        if row[1] == 'translations':
            continue
        lirbantu = row[0]
        russian = row[1]
        pos = row[2]
        spheres = row[3]
        if spheres:
            spheres = spheres.split(', ')
        else:
            spheres = []
        etymology = row[4]
        comment = row[5]
        tmp = {
            "lirbantu": lirbantu,
            "russian": russian,
            "pos": pos,
            "spheres": spheres,
            "etymology": etymology,
            "comment": comment,

            "root1": "",
            "root2": "",
            "logic": "",
            "grammar": "",
            "root1_emoji": "",
            "root2_emoji": "",
            "description": "",
        }
        dictionary.append(tmp)
    return dictionary


def main():
    sheet = get_raw_sheet()
    dictionary = sheet_to_dictionary(sheet)
    save_new_dictionary(dictionary)


if __name__ == '__main__':
    main()
