import os
import requests
from pathlib import Path

from lirbantu.src.project import get_project_dir


def emoji_to_svg(emoji_char, output_path=None, cache_dir=None):
    """
    Convert a single emoji character to an SVG file and save it locally.
    Works offline after the first download (cached).

    Args:
        emoji_char (str): A single emoji character (e.g., '😊')
        output_path (str or Path): Where to save the SVG file
        cache_dir (str or Path, optional): Directory to cache SVGs for offline use.
                                          Defaults to ~/.cache/emoji_svgs/

    Returns:
        bool: True if successful, False otherwise
    """
    # Set up cache directory
    if cache_dir is None:
        cache_dir = Path.home() / '.cache' / 'emoji_svgs'
    else:
        cache_dir = Path(cache_dir)

    cache_dir.mkdir(parents=True, exist_ok=True)

    # Get the Unicode codepoint for the emoji (e.g., '1f60a' for 😊)
    codepoint = format(ord(emoji_char), 'x')
    cached_svg = cache_dir / f"{codepoint}.svg"
    if output_path is None:
        root = get_project_dir()
        output_path = f'{root}/emojis/{codepoint}.svg'

    # If we already have it cached, just copy it
    if cached_svg.exists():
        import shutil
        shutil.copy2(cached_svg, output_path)
        return True

    # Otherwise, download from Twemoji (Twitter's open-source emoji set)
    # Twemoji provides clean, well-designed SVG emojis
    url = f"https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/{codepoint}.svg"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Save to cache
        with open(cached_svg, 'wb') as f:
            f.write(response.content)

        # Copy to desired output location
        with open(output_path, 'wb') as f:
            f.write(response.content)

        return True

    except requests.RequestException as e:
        print(f"Error downloading emoji: {e}")
        return False
