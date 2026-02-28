from lirbantu.config.config import get_usable_emojis
from lirbantu.emoji_to_svg import emoji_to_svg


def main():
    emojis = get_usable_emojis()
    for emoji in emojis:
        success = emoji_to_svg(emoji)
        if success:
            print('.', end='')
        else:
            print('-', end='')


if __name__ == '__main__':
    main()
