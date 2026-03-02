from emoji_font_generator.input.config import get_dictionary
from emoji_font_generator.word import Word


class TestConfig:

    def test_can_get_typed_dictionary(self):
        dct = get_dictionary()

        assert type(dct) is list
        assert type(dct[0]) is Word
