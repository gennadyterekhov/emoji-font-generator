from lirbantu.combine import combine4
from lirbantu.helpers import get_twemoji_codepoint


def test_combine():
    combine4('банк', ['💰','🏛','genitive','noun'])
    # check that svg can be viewed in intellij idea



def main():
    test_combine()


if __name__ == '__main__':
    main()
