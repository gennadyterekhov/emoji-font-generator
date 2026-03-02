from emoji_font_generator.combine import combine_wordform


class TestCombine:

    def test_combine(self):
        print('skipped. only manual launch because changes svgs')
        return
        wf = get_wordform_from_ai_dictionary('банк')
        combine_wordform(wf)

        wf = get_wordform_from_ai_dictionary('лечить')
        combine_wordform(wf)

        wf = get_wordform_from_ai_dictionary('хороший')
        combine_wordform(wf)

        wf = get_wordform_from_ai_dictionary('верующий')
        combine_wordform(wf)

        # check that svg can be viewed in intellij idea


