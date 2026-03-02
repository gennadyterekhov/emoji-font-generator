import os
import time

from dotenv import load_dotenv

from emoji_font_generator.input.config import get_dictionary, save_new_dictionary, get_llm_config_from_env, LlmConfig
from emoji_font_generator.llm.llm import add_emojis_to_one_word


def add_emojis_to_dictionary(llm_config: LlmConfig) -> None:
    dct = get_dictionary()
    # words are not unique (can have several orthographic variants or meaning), we must control uniqueness at app level
    used_words = {}
    # list of words with errors. we need this to skip useless llm requests
    unused_words = {}

    pos_whitelist = ['num', 'prep', 'interj', 'pron', 'conj']

    for i, word in enumerate(dct):
        conlang_word = word['conlang']
        natural_word = word['natural']

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
        tmp = add_emojis_to_one_word(llm_config, word)
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
    try:
        llm_config = get_llm_config_from_env()
        add_emojis_to_dictionary(llm_config)
    except KeyboardInterrupt:
        print('exiting')


if __name__ == "__main__":
    main()
