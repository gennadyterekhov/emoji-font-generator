import inspect

if not hasattr(inspect, 'getargspec'):
    def _getargspec(func):
        spec = inspect.getfullargspec(func)
        return spec.args, spec.varargs, spec.varkw, spec.defaults


    inspect.getargspec = _getargspec  # pymorphy2 0.9 needs getargspec, removed in py3.11+

from emoji_font_generator.word import Word
import pymorphy2


def get_all_cases(word):
    morph = pymorphy2.MorphAnalyzer()
    """Returns dict with all 6 grammatical cases for a Russian word"""
    parse = morph.parse(word)[0]  # Take first (most likely) parse

    cases = {
        'nominative': word,  # исходная форма
        'genitive': parse.inflect({'gent'}).word if parse.inflect({'gent'}) else None,
        'dative': parse.inflect({'datv'}).word if parse.inflect({'datv'}) else None,
        'accusative': parse.inflect({'accs'}).word if parse.inflect({'accs'}) else None,
        'instrumental': parse.inflect({'ablt'}).word if parse.inflect({'ablt'}) else None,
        'prepositional': parse.inflect({'loct'}).word if parse.inflect({'loct'}) else None,
    }
    return cases


def get_additional_wordforms(w: Word) -> list[Word]:
    cases = get_all_cases(w.natural)
    wfs = []
    for case, case_form in cases.items():
        if case_form:
            tmp_word = Word(
                conlang=w.conlang,
                natural=case_form,
                pos=w.pos,
                spheres=w.spheres,
                etymology=w.etymology,
                comment=w.comment,
                root1=w.root1,
                root2=w.root2,
                logic=w.logic,
                grammar=case,
                root1_emoji=w.root1_emoji,
                root2_emoji=w.root2_emoji,
                description=w.description,
            )
            wfs.append(tmp_word)
    return wfs
