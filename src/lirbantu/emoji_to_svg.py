import os
import time

import requests
from pathlib import Path

from lirbantu.project import get_project_dir


def emoji_to_svg(emoji_char, output_path=None):
    codepoint = get_twemoji_codepoint(emoji_char)
    if output_path is None:
        root = get_project_dir()
        output_path = f'{root}/emojis/twemoji/{codepoint}.svg'
    if Path(output_path).exists():
        return True

    # Otherwise, download from Twemoji (Twitter's open-source emoji set)
    # Twemoji provides clean, well-designed SVG emojis
    url = f"https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/{codepoint}.svg"

    try:
        print()
        print(f'Downloading twemoji for {emoji_char} = {codepoint} from {url}')
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Copy to desired output location
        with open(output_path, 'wb') as f:
            f.write(response.content)
        # cooldown
        time.sleep(0.2)
        return True

    except requests.RequestException as e:
        print(f"Error downloading emoji: {e}")
        return False


def get_twemoji_codepoint(emoji_char, ):
    total = ''
    for char in emoji_char:
        codepoint = format(ord(char), 'x')
        total += f'-' + codepoint
    return total[1:]
