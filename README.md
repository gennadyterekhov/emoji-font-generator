# emoji-font-generator 

This project allows automated creation of hieroglyphic script using emojis or custom svgs.

Examples use lirbantu (conlang) with a russian dictionary.

# Idea
the base idea is to encode every word using one hieroglyph consisting of 1-4 parts

- character 1 (any svg)
- character 2 (any svg) (optional)
- logical properties. how the characters relate to each other (any svg) (optional)
- grammar. what grammatical properties does this word have. singluar/plural, declension, conjugation etc. (any svg) (optional)

## Examples:  
'eye' -> '👁' (emoji is literal)  
'rain' ->
```json
        {
                "character 1": "☁️",
                "character 2": "💧",
                "logic": "🟢 (genitive, you can represent it with any custom svg/emoji)",
                "grammar": "🟣 (noun singular, you can represent it with any custom svg/emoji)",
                "description": "cloud water, water of the cloud, water from the cloud"
        }
```


we can then combine svgs into a single composite character.

# Usage

- create a dictionary for your language (list of words to use). convenient to use Google Sheets for this.
- use https://onlinetsvtools.com/convert-tsv-to-json to convert your dictionary sheet to json. put it it `input/raw/sheet.json`
- use `cmd/sheet_to_dictionary.py` (or write your own converter) to convert your raw sheet to a dictionary.json-compatible format.
- create emoji correspondence for your roots. You can use an LLM manually in browser (free), or use a token with `cmd/add_emojis_to_dictionary.py`
  - set llm vars in .env
    - LLM_URL (completions api)
    - LLM_API_KEY
    - LLM_MODEL_NAME
  - example prompt is in `input/llm/prompt_for_1_word.md`
- download emoji svgs (`cmd/download_all_emoji_svgs_from_twemoji.py`)
- if needed, create custom svgs if emojis are not enough. this site is handy https://text-to-svg.com/
- create combined svgs prom parts, according to the logic (`cmd/create_combined_svgs.py`)
- move your font to `input/fonts/input_font.ttf`. you can use any font as a 'base', so that any other characters are printable
- add ligatures for hieroglyphs (`cmd/add_ligatures.py`) . font will be saved in `output/fonts/output_font.ttf`
