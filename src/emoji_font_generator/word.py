import json
from dataclasses import fields, asdict

from pydantic import Field
from pydantic.dataclasses import dataclass as pydantic_dataclass


@pydantic_dataclass
class Word:
    conlang: str = ''
    natural: str = ''
    pos: str = ''
    spheres: list[str] = Field(default_factory=list)
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

    def to_json(self):
        d={**asdict(self)}
        return json.dumps(d)

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
