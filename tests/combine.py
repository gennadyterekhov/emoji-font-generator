from lirbantu.combine import combine4, combine_wordform
from lirbantu.config.config import get_wordform_from_ai_dictionary
from lirbantu.helpers import get_twemoji_codepoint


def test_combine():
    wf=get_wordform_from_ai_dictionary('банк')
    combine_wordform(wf)

    wf=get_wordform_from_ai_dictionary('лечить')
    combine_wordform(wf)

    wf=get_wordform_from_ai_dictionary('хороший')
    combine_wordform(wf)

    wf=get_wordform_from_ai_dictionary('строящий')
    combine_wordform(wf)

    # check that svg can be viewed in intellij idea



def main():
    test_combine()


if __name__ == '__main__':
    main()
