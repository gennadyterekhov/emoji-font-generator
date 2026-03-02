from dataclasses import dataclass, fields


@dataclass
class Word:
    conlang: str
    natural: str
    pos: str
    spheres: list[str]
    etymology: str
    comment: str
    root1: str
    root2: str
    logic: str
    grammar: str
    root1_emoji: str
    root2_emoji: str
    description: str

    def get_id(self):
        return f'{self.conlang}_{self.natural}_{self.pos}'

    def get(self, name, default=None):
        val = Word.get_field_by_name(self, name)
        if val:
            return val
        return default

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
