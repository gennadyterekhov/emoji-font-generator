from lirbantu.helpers import get_twemoji_codepoint


def test_codepoint():
    cdp = get_twemoji_codepoint('😊')
    assert (cdp == '1f60a')

    cdp = get_twemoji_codepoint('✍️')
    assert (cdp == '270d-fe0f')

    cdp = get_twemoji_codepoint('👎')
    assert (cdp == '1f44e')

    cdp = get_twemoji_codepoint('🇧🇭')
    assert (cdp == '1f1e7-1f1ed')


def main():
    test_codepoint()


if __name__ == '__main__':
    main()
