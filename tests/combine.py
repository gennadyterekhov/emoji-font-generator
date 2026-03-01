from emoji_font_generator.combine import  combine_wordform
from emoji_font_generator.config.config import get_wordform_from_ai_dictionary


def test_combine():
    wf=get_wordform_from_ai_dictionary('банк')
    combine_wordform(wf)

    wf=get_wordform_from_ai_dictionary('лечить')
    combine_wordform(wf)

    wf=get_wordform_from_ai_dictionary('хороший')
    combine_wordform(wf)

    wf=get_wordform_from_ai_dictionary('верующий')
    combine_wordform(wf)

    # check that svg can be viewed in intellij idea



def main():
    test_combine()


if __name__ == '__main__':
    main()
