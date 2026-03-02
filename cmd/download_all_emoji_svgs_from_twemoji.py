from emoji_font_generator.download import download_svg_from_twemoji
from emoji_font_generator.input.config import get_emojis_used_by_ai


def download_list(emojis):
    failures = 0
    for emoji in emojis:
        if emoji:
            success = download_svg_from_twemoji(emoji)
            if not success:
                failures += 1
    print(f'failures {failures}')


def main():
    download_list(get_emojis_used_by_ai())


if __name__ == '__main__':
    main()
