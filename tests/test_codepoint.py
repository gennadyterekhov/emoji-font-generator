from emoji_font_generator.helpers import get_twemoji_codepoint


class TestCodepoint:
    def test_codepoint():
        cdp = get_twemoji_codepoint('😊')
        assert (cdp == '1f60a')

        cdp = get_twemoji_codepoint('✍️')
        assert (cdp == '270d-fe0f')

        cdp = get_twemoji_codepoint('👎')
        assert (cdp == '1f44e')

        cdp = get_twemoji_codepoint('🇧🇭')
        assert (cdp == '1f1e7-1f1ed')
