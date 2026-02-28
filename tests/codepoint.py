from lirbantu.emoji_to_svg import get_twemoji_codepoint


def test_codepoint():
    cdp = get_twemoji_codepoint('😊')
    assert (cdp == '1f60a')

    cdp = get_twemoji_codepoint('✍️')
    assert (cdp == '270d-fe0f')

    cdp = get_twemoji_codepoint('👎')
    assert (cdp == '1f44e')


def main():
    test_codepoint()


if __name__ == '__main__':
    main()
