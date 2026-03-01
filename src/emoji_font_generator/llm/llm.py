import json

import requests

from emoji_font_generator.input.io import read_md_file
from emoji_font_generator.project import get_project_dir


def ask_ai(api_key: str, model_name: str, base_url: str, prompt: str) -> str:
    response = requests.post(
        url=base_url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,  # "How many r's are in the word 'strawberry'?"
                }
            ],
            "reasoning": {"enabled": True}
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
