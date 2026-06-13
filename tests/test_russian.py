from emoji_font_generator.russian import get_additional_wordforms
from emoji_font_generator.word import Word


class TestRussian:
    def test_russian(self):
        """
        uv run pytest -s tests/test_russian.py::TestRussian::test_russian
        """
        wfs = get_additional_wordforms(Word(natural='конь'))

        assert (wfs[0].natural == 'конь')
        assert (wfs[0].grammar == 'nominative')

        assert (wfs[1].natural == 'коня')
        assert (wfs[1].grammar == 'genitive')

        assert (wfs[2].natural == 'коню')
        assert (wfs[2].grammar == 'dative')

        assert (wfs[3].natural == 'коня')
        assert (wfs[3].grammar == 'accusative')

        assert (wfs[4].natural == 'конём')
        assert (wfs[4].grammar == 'instrumental')

        assert (wfs[5].natural == 'коне')
        assert (wfs[5].grammar == 'prepositional')

