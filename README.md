# emoji-font-generator 

This project allows automated creation of hieroglyphic script using emojis or custom svgs.

So, as a result, your alphabetic text (in a natural language or a conlang) will look like logographic text, without actually having unique unicode characters.

Examples use lirbantu (conlang) with a russian dictionary.

# Idea
the base idea is to encode every word using one hieroglyph consisting of 1-4 parts

- character 1 (any svg)
- character 2 (any svg) (optional)
- logical properties. how the characters relate to each other (any svg) (optional)
- grammar. what grammatical properties does this word have. singluar/plural, declension, conjugation etc. (any svg) (optional)

## Examples:  
'eye' -> '👁' (emoji is literal)  
'white' ->
```json
        {
                "character 1": "🎨",
                "character 2": "💡",
                "logic": "< (genitive, you can represent it with any custom svg/emoji)",
                "grammar": "o (adjective singular, you can represent it with any custom svg/emoji)",
                "description": "light's color, color of the light"
        }
```

we can then combine svgs into a single composite character.
resulting svg:

![white](input/emojis/combined/белый.svg)


[//]: # (<?xml version='1.0' encoding='utf-8'?>)

[//]: # (<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400" version="1.1"><!--description: вода из облаков --><path fill="#CCD6DD" d="M27 8c-.701 0-1.377.106-2.015.298.005-.1.015-.197.015-.298 0-3.313-2.687-6-6-6-2.769 0-5.093 1.878-5.785 4.427C12.529 6.154 11.783 6 11 6c-3.314 0-6 2.686-6 6 0 3.312 2.686 6 6 6 2.769 0 5.093-1.878 5.785-4.428.686.273 1.432.428 2.215.428.375 0 .74-.039 1.096-.104-.058.36-.096.727-.096 1.104 0 3.865 3.135 7 7 7s7-3.135 7-7c0-3.866-3.135-7-7-7z" transform="translate&#40;0, 0&#41; scale&#40;5, 8&#41;" /><path fill="#E1E8ED" d="M31 22c-.467 0-.91.085-1.339.204.216-.526.339-1.1.339-1.704 0-2.485-2.015-4.5-4.5-4.5-1.019 0-1.947.351-2.701.921C22.093 14.096 19.544 12 16.5 12c-2.838 0-5.245 1.822-6.131 4.357C9.621 16.125 8.825 16 8 16c-4.418 0-8 3.582-8 8 0 4.419 3.582 8 8 8h23c2.762 0 5-2.238 5-5s-2.238-5-5-5z" transform="translate&#40;0, 0&#41; scale&#40;5, 8&#41;" /><path fill="#5DADEC" d="M28.344 17.768L18.148 1.09 8.7 17.654c-2.2 3.51-2.392 8.074-.081 11.854 3.285 5.373 10.363 7.098 15.811 3.857 5.446-3.24 7.199-10.22 3.914-15.597z" transform="translate&#40;200, 0&#41; scale&#40;5, 8&#41;" /><defs transform="translate&#40;75, 275&#41;" /><g fill="#000000" transform="translate&#40;75, 275&#41;"><g transform="translate&#40;0, 0&#41;"><path d="M0 29.61L0 25.51L23.71 15.50L23.71 19.87L4.91 27.59L23.71 35.38L23.71 39.75L0 29.61Z" /></g></g><defs transform="translate&#40;275, 275&#41;" /><g fill="#000000" transform="translate&#40;275, 275&#41;"><g transform="translate&#40;0, 0&#41;"><path d="M0 34.52L0 30.10L13.50 30.10L13.50 34.52L0 34.52Z" /></g></g></svg>)


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
- if needed, create custom svgs if emojis are not enough.
  - this site is handy https://text-to-svg.com/
  - use `cmd/font_to_svgs.py` to convert a font to a list of svgs
- create combined svgs prom parts, according to the logic (`cmd/create_combined_svgs.py`)
- move your font to `input/fonts/input_font.ttf`. you can use any font as a 'base', so that any other characters are printable
- add ligatures for hieroglyphs (`cmd/add_ligatures.py`) . font will be saved in `output/fonts/output_font.ttf`
