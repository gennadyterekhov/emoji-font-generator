
from lirbantu.config.config import get_usable_emojis
from lirbantu.emoji_to_svg import emoji_to_svg


def main():
    emojis = get_usable_emojis()
    for emoji in emojis:
        emoji_to_svg(emoji)

if __name__ == '__main__':
    main()