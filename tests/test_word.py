import json

from emoji_font_generator.word import Word


class TestWord:

    def test_can_get_from_json(self):
        tmp = {
            "conlang": 'conlang',
            "natural": 'natural',
            "pos": 'pos',
            "spheres": ['spheres'],
            "etymology": 'etymology',
            "comment": 'comment',
        }
        word = Word(**tmp)
        assert word.conlang == 'conlang'
        assert word.natural == 'natural'

    def test_can_encode_json(self):
        tmp = {"conlang": 'conlang', }
        word = Word(**tmp)
        raw = word.to_json()
        assert raw == '{"conlang": "conlang", "natural": "", "pos": "", "spheres": [], "etymology": "", "comment": "", "root1": "", "root2": "", "logic": "", "grammar": "", "root1_emoji": "", "root2_emoji": "", "description": ""}'
