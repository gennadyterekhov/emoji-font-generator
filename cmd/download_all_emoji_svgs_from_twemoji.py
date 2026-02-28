from lirbantu.config.config import get_usable_emojis, get_emojis_used_by_ai
from lirbantu.emoji_to_svg import emoji_to_svg


def download_list(emojis):
    failures=0
    for emoji in emojis:
        success = emoji_to_svg(emoji)
        if not success:
            failures+=1
    print(f'failures {failures}')

def main():
    download_list(get_usable_emojis())
    download_list(get_emojis_used_by_ai())


if __name__ == '__main__':
    main()
