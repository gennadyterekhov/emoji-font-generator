import json
from dataclasses import fields, asdict, dataclass, field

from pydantic import Field
from pydantic.dataclasses import dataclass as pydantic_dataclass


@dataclass
class Word:
    conlang: str = ''
    natural: str = ''
    pos: str = ''
    spheres: list[str] = field(default_factory=list)
    etymology: str = ''
    comment: str = ''
    root1: str = ''
    root2: str = ''
    logic: str = ''
    grammar: str = ''
    root1_emoji: str = ''
    root2_emoji: str = ''
    description: str = ''

    def get_id(self):
        return f'{self.conlang}_{self.natural}_{self.pos}'

    def get(self, name, default=None):
        val = Word.get_field_by_name(self, name)
        if val:
            return val
        return default

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=8, ensure_ascii=False)

    def to_dict(self) -> dict:
        return asdict(self)

    def __str__(self):
        return self.get_id()

    def __repr__(self):
        return f'<Word {self.get_id()}>'

    def __get__(self, name, default=None):
        val = Word.get_field_by_name(self, name)
        if val:
            return val
        return default

    @staticmethod
    def get_field_by_name(cls, field_name):
        for field in fields(cls):
            if field.name == field_name:
                return field
        return None
