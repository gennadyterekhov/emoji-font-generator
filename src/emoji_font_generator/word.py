import dataclasses


@dataclasses.dataclass
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
