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
        if 'content' in ai_response:
            md_json = ai_response['content']
            structured_response = md_json.replace('```json', '')
            structured_response = structured_response.replace('```', '')
            structured_response = json.loads(structured_response)
        else:
            print('unexpected response', ai_response)
            return None

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
    # words are not unique (can have several orthographic variants or meaning), we must control uniqueness at app level
    used_words = {}
    # list of words with errors. we need this to skip useless llm requests
    unused_words = {}

    pos_whitelist = ['num', 'prep', 'interj', 'pron', 'conj']

    for i, word in enumerate(dct):
        conlang_word = word['lirbantu']
        natural_word = word['russian']

        if word['pos'] in pos_whitelist:
            continue

        # check for already processed word first, so that we can populate used_words correctly when starting again
        # note the absence of continue
        if word['root1'] or word['root2']:
            used_words[natural_word] = word
            used_words[conlang_word] = word

        if natural_word in used_words:
            dct[i] = used_words[natural_word]
            # we save on every iteration so that we can abort the long-running process and then continue from where we left
            save_new_dictionary(dct)
            continue

        if conlang_word in used_words:
            dct[i] = used_words[conlang_word]
            # we save on every iteration so that we can abort the long-running process and then continue from where we left
            save_new_dictionary(dct)
            continue

        if natural_word in unused_words:
            continue

        if conlang_word in unused_words:
            continue

        print(f'processing word {conlang_word}={natural_word} {i}/{len(dct)}')

        # let the llm rest a little
        time.sleep(1)
        tmp = add_emojis_to_one_word(api_key, model_name, base_url, word)
        if tmp:
            dct[i] = tmp
            # we save on every iteration so that we can abort the long-running process and then continue from where we left
            save_new_dictionary(dct)
            used_words[natural_word] = tmp
            used_words[conlang_word] = tmp
        else:
            unused_words[natural_word] = word
            unused_words[conlang_word] = word
    save_new_dictionary(dct)


def main():
    load_dotenv()
    api_key = os.getenv('LLM_API_KEY')
    model_name = os.getenv('LLM_MODEL_NAME')
    base_url = os.getenv('LLM_URL')
    add_emojis_to_dictionary(api_key, model_name, base_url)


if __name__ == "__main__":
    main()
