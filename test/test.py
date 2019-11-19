import sys,os
import unittest
import json
from main import parse_text,compare_two_text,reparse_text,ld,parse_ld,handler

class TestParse(unittest.TestCase):
    def test_single_noun(self):
        result = parse_text('東京')
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['word'],'東京')
        self.assertEqual(result[0]['reading'],'トウキョウ')
        self.assertEqual(result[0]['type'],'名詞')

    def test_multiple_noun(self):
        result = parse_text('東京スカイツリー')
        self.assertEqual(len(result),3)
        
    def test_text(self):
        result = parse_text('プラスチックと燃えるゴミ')
        self.assertEqual(len(result),4)
        self.assertEqual(result[1]['type'], '助詞')
        self.assertEqual(result[2]['type'], '動詞')

    def test_user_dic(self):
        result = parse_text('資源ごみ')
        self.assertEqual(len(result),1)

class TestCompare(unittest.TestCase):
    def test_reparse_text_single_noun(self):
        #配列に名詞しかない場合はすべてそのまま返ってくる
        result = reparse_text([{'word': '燃えるゴミ', 'reading': 'モエルゴミ', 'type': '名詞'}])
        self.assertEqual(len(result),1)
        self.assertEqual(result[0],{'word': '燃えるゴミ', 'reading': 'モエルゴミ', 'type': '名詞'})

    def test_reparse_text_multiple_noun(self):
        #配列に名詞しかない場合はすべてそのまま返ってくる
        result = reparse_text([
            {'word': '燃えるゴミ', 'reading': 'モエルゴミ', 'type': '名詞'},
            {'word': '燃えないゴミ', 'reading': 'モエナイゴミ', 'type': '名詞'},
        ])
        self.assertEqual(len(result),2)

    def test_reparse_text_verb_noun(self):
        #動詞があれば名詞につなぐ
        result = reparse_text([
            {'word': '走る', 'reading': 'ハシル', 'type': '動詞'},
            {'word': '車', 'reading': 'クルマ', 'type': '名詞'},
        ])

        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['word'], '走る車')
        self.assertEqual(result[0]['reading'], 'ハシルクルマ')
        self.assertEqual(result[0]['type'], '名詞')

    def test_reparse_text_multiple_comb(self):
        #動詞/形容詞/連体詞/助動詞/があれば名詞につなぐ
        result = reparse_text([
            {'word': '走る', 'reading': 'ハシル', 'type': '動詞'},
            {'word': '車', 'reading': 'クルマ', 'type': '名詞'},
            {'word': 'と', 'reading': 'ト', 'type': '助詞'},
            {'word': '古い', 'reading': 'フルイ', 'type': '形容詞'},
            {'word': '雑誌', 'reading': 'ザッシ', 'type': '名詞'},
            {'word': 'と', 'reading': 'ト', 'type': '助詞'},
            {'word': '燃え', 'reading': 'モエ', 'type': '動詞'},
            {'word': 'ない', 'reading': 'ナイ', 'type': '助動詞'},
            {'word': 'ゴミ', 'reading': 'ゴミ', 'type': '名詞'},
            {'word': 'と', 'reading': 'ト', 'type': '助詞'},
            {'word': '大きな', 'reading': 'オオキナ', 'type': '連体詞'},
            {'word': 'ゴミ', 'reading': 'ゴミ', 'type': '名詞'},
        ])

        self.assertEqual(len(result),4)
        self.assertEqual(result[0]['word'], '走る車')
        self.assertEqual(result[1]['word'], '古い雑誌')
        self.assertEqual(result[2]['word'], '燃えないゴミ')
        self.assertEqual(result[3]['word'], '大きなゴミ')

class TestLd(unittest.TestCase):
    def test_ld(self):
        score = ld('モエルゴミ','モエナイゴミ')
        self.assertEqual(score,2)
    
    def test_parse_ld(self):
        score = parse_ld(['モエナイゴミ'], ['モエルゴミ'])
        self.assertEqual(score, round(1-2/6,2))

    def test_single_multi_parse_ld(self):
        score = parse_ld(['ビン'], ['ビン','カン','ペットボトル'])
        self.assertEqual(score, 1)

    def test_multi_multi_parse_ld(self):
        score = parse_ld(['ビン','アキカン'], ['ビン','カン','ペットボトル'])
        self.assertEqual(score, 0.75)

    def test_nomatch_arse_ld(self):
        score = parse_ld(['フクロ'], ['ビン','カン','ペットボトル'])
        self.assertEqual(score, 0)

class TestHandler(unittest.TestCase):
    def test_compare_two_text(self):
        score = compare_two_text('燃えるゴミ','燃えないゴミ')
        self.assertEqual(score, round(1-2/6,2))

    def test_single_single(self):
        result = handler({'resource':'/compare','queryStringParameters':{'text1':'燃えるゴミ','text2':'燃えないゴミ'}},{})
        self.assertEqual(result['statusCode'],200)
        self.assertEqual(json.loads(result['body']),{'score': round(1-2/6,2)})

    def test_multi_multi(self):
        result = handler({'resource':'/compare','queryStringParameters':{'text1':'瓶と雑誌','text2':'ビンカンペットボトル'}},{})
        self.assertEqual(result['statusCode'],200)

if __name__ == '__main__':
    unittest.main()