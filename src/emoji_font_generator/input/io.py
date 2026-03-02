import json
from pathlib import Path


def write_json_file(path: Path | str, data) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=8, ensure_ascii=False)


def read_json_file(path: Path | str):
    with open(path) as json_file:
        data = json.load(json_file)
    return data


def read_md_file(path: Path | str):
    with open(path) as md_file:
        data = md_file.read()
    return data
