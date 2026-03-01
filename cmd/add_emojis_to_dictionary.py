import json
import os
import time
from typing import Optional

from dotenv import load_dotenv

from emoji_font_generator.input.config import get_dictionary, save_new_dictionary
from emoji_font_generator.llm.llm import ask_ai, get_prompt_for_one_word


def add_emojis_to_one_word(api_key: str, model_name: str, base_url: str, word: dict) -> Optional[dict]:
    data_for_prompt = {
        "word": word['russian'],
        "logic": [
            "and",
            "or",
            "not",
            "genitive",
            "accusative",
            "instrumental"
        ],
        "grammar": [
            "adv",
            "adj",
            "n",
            "plural",
            "v",
            "imperative",
            "pr part",
            "past part",
            "diminutive",
            "augmentative",
            "causative"
        ]
    }
    prompt = get_prompt_for_one_word(data_for_prompt)
    try:
        ai_response = ask_ai(api_key, model_name, base_url, prompt)
        structured_response = json.loads(ai_response)
        if 'error' in structured_response:
            print(f'error classifying word {word['lirbantu']}={word['russian']}, error: {structured_response["error"]}')
            return None
        word['root1'] = structured_response.get('root1', '')
        word['root2'] = structured_response.get('root2', '')
        word['logic'] = structured_response.get('logic', '')
        word['grammar'] = structured_response.get('grammar', '')
        word['root1_emoji'] = structured_response.get('root1_emoji', '')
        word['root2_emoji'] = structured_response.get('root2_emoji', '')
        word['description'] = structured_response.get('description', '')

    except Exception as e:
        print(f'could not decode ai response for word {word['lirbantu']}={word['russian']}, error: {e}')
        return None

    return word


def add_emojis_to_dictionary(api_key: str, model_name: str, base_url: str) -> None:
    dct = get_dictionary()
    updated = []
    # words are not unique (can have several orthographic variants or meaning), we must control uniqueness at app level
    used_words = set()
    for i, word in enumerate(dct):
        if word['russian'] in used_words:
            continue
        if word['lirbantu'] in used_words:
            continue

        print(f'processing word {word('lirbantu')} {i}/{len(dct)}')

        # let the llm rest a little
        time.sleep(1)
        tmp = add_emojis_to_one_word(api_key, model_name, base_url, word)
        if tmp:
            updated.append(tmp)
        used_words.add(word['russian'])
        used_words.add(word['lirbantu'])
    save_new_dictionary(updated)


def main():
    load_dotenv()
    api_key = os.getenv('LLM_API_KEY')
    model_name = os.getenv('LLM_MODEL_NAME')
    base_url = os.getenv('LLM_URL')
    add_emojis_to_dictionary(api_key, model_name, base_url)


if __name__ == "__main__":
    main()
