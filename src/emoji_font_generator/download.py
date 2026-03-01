import time

import requests
from pathlib import Path

from emoji_font_generator.helpers import get_twemoji_codepoint
from emoji_font_generator.project import get_project_dir


def download_svg_from_twemoji(emoji_char, output_path=None) -> bool:
    codepoint = get_twemoji_codepoint(emoji_char)
    if output_path is None:
        root = get_project_dir()
        output_path = f'{root}/input/emojis/twemoji/{codepoint}.svg'
    if Path(output_path).exists():
        print('Already exists')
        return True

    # (Twitter's open-source emoji set)
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
        # cooldown to prevent abuse
        time.sleep(0.2)
        return True

    except requests.RequestException as e:
        print(f"Error downloading emoji: {e}")
        return False
