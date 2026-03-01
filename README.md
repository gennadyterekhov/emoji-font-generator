# automated creation of hieroglyphic script using emojis or custom svgs 

examples use lirbantu (conlang)

# idea


# emojis for roots are generated with an LLM manually (in browser)
prompt is in config/prompt.md

# usage

- create a dictionary for your language (list of words to use)
- create emoji correspondence for your roots. You can use an LLM, example prompt is in `config/prompt.md`
- download emoji svgs (`cmd/download_all_emoji_svgs_from_twemoji.py`)
- if needed, create custom svgs if emojis are not enough. this site is handy https://text-to-svg.com/
- create combined svgs prom parts, according to the logic (`cmd/create_combined_svgs.py`)
- move your font to `input`. you can use any font as a 'base', so that any other characters are printable
- add ligatures for hieroglyphs (`cmd/add_ligatures.py`) . font will be saved in `output`

# what to do next?

- normalize dictionary
- add swadesh list words
- export dictionary
- reassign emojis meaningfully
- generate svgs
- generate font