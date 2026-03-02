import json
from typing import Optional

import requests

from emoji_font_generator.input.config import LlmConfig
from emoji_font_generator.input.io import read_md_file
from emoji_font_generator.project import get_project_dir


def ask_ai(llm_config: LlmConfig, prompt: str) -> str | dict:
    response = requests.post(
        url=llm_config.base_url,
        headers={
            "Authorization": f"Bearer {llm_config.api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": llm_config.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,  # "How many r's are in the word 'strawberry'?"
                }
            ],
            "reasoning": {"enabled": llm_config.use_reasoning}
        })
    )

    # Extract the assistant message with reasoning_details
    response = response.json()
    response = response['choices'][0]['message']
    return response


def get_prompt_for_one_word(input_data: dict) -> str:
    root = get_project_dir()
    path = f'{root}/input/llm/prompt_for_1_word.md'
    raw_prompt = read_md_file(path)

    return raw_prompt.replace('{{{input_data}}}', json.dumps(input_data))


def add_emojis_to_one_word(llm_config: LlmConfig, word: dict) -> Optional[dict]:
    data_for_prompt = {
        "word": word['natural'],
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
    ai_response = ''
    try:
        ai_response = ask_ai(llm_config, prompt)
        if 'content' in ai_response:
            md_json = ai_response['content']
            structured_response = md_json.replace('```json', '')
            structured_response = structured_response.replace('```', '')
            structured_response = json.loads(structured_response)
        else:
            print('unexpected response', ai_response)
            return None

        if 'error' in structured_response:
            print(f'error classifying word {word['conlang']}={word['natural']}, error: {structured_response["error"]}')
            return None
        word['root1'] = structured_response.get('root1', '')
        word['root2'] = structured_response.get('root2', '')
        word['logic'] = structured_response.get('logic', '')
        word['grammar'] = structured_response.get('grammar', '')
        word['root1_emoji'] = structured_response.get('root1_emoji', '')
        word['root2_emoji'] = structured_response.get('root2_emoji', '')
        word['description'] = structured_response.get('description', '')

    except Exception as e:
        print(f'could not decode ai response for word {word['conlang']}={word['natural']}')
        print(f'error: {e}')
        print(f'ai_response: {ai_response}')
        return None

    return word
