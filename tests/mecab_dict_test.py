from app.mecab_dict import parse_to_noun_from_custom_dict,reparse_text,is_negative,is_Taigigo
import unittest

class ParseToNoun(unittest.TestCase):
    def test_single_noun(self):
        result = parse_to_noun_from_custom_dict('東京')
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['word'],'東京')
        self.assertEqual(result[0]['reading'],'トウキョウ')
        self.assertEqual(result[0]['type'],'名詞')

    def test_multiple_noun(self):
        result = parse_to_noun_from_custom_dict('東京スカイツリー')
        self.assertEqual(len(result),3)
        
    def test_text(self):
        result = parse_to_noun_from_custom_dict('プラスチックと燃えるゴミ')
        self.assertEqual(len(result),4)
        self.assertEqual(result[1]['type'], '助詞')
        self.assertEqual(result[2]['type'], '動詞')

    def test_user_dic(self):
        result = parse_to_noun_from_custom_dict('資源ごみ')
        self.assertEqual(len(result),1)

class ReparseText(unittest.TestCase):
    def test_single_noun(self):
        result = reparse_text([{'word': 'ごみ','reading':'ゴミ','type': '名詞'}])
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['word'],'ごみ')
        self.assertEqual(result[0]['reading'],'ゴミ')
        self.assertEqual(result[0]['type'],'名詞')

    def test_reparse_text_multiple_noun(self):
        #配列に名詞しかない場合はすべてそのまま返ってくる
        result = reparse_text([
            {'word': '燃えるゴミ', 'reading': 'モエルゴミ', 'type': '名詞'},
            {'word': '燃えないゴミ', 'reading': 'モエナイゴミ', 'type': '名詞'},
        ])
        self.assertEqual(len(result),2)

    def test_link_noun(self):
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

    def test_none_noun(self):
        result = reparse_text([{'word': '燃える','reading':'モエル','type': '動詞'},{'word': '高い','reading':'タカイ','type': '形容詞'}])
        self.assertEqual(len(result),0)

class IsNegative(unittest.TestCase):
    def test_noun(self):
        self.assertTrue(is_negative('不常\tフジョウ\tフジョウ\t名詞-普通詞'))
        self.assertTrue(is_negative('無情\tムジョウ\tムジョウ\t名詞-普通詞'))
        self.assertTrue(is_negative('未曾有\tミゾウ\tミゾウ\t名詞-普通詞'))
        self.assertTrue(is_negative('反抗\tハンコウ\tハンコウ\t名詞-普通詞'))
        self.assertTrue(is_negative('異質\tイシツ\tイシツ\t名詞-普通詞'))
        self.assertTrue(is_negative('無い\tナイ\tナイ\t名詞-普通詞'))
        self.assertFalse(is_negative('意味\tイミ\tイミ\t名詞-普通詞'))
    
    def test_adjective(self):
        self.assertTrue(is_negative('無い\tナイ\tナイ\t形容詞'))
        self.assertTrue(is_negative('ない\tナイ\tナイ\t形容詞'))
        self.assertFalse(is_negative('大きい\tオオキイ\tオオキイ\t形容詞'))

    def test_axverb(self):
        self.assertTrue(is_negative('ない\tナイ\tナイ\t助動詞'))
        self.assertTrue(is_negative('ぬ\tヌ\tヌ\t助動詞'))
        self.assertTrue(is_negative('ん\tン\tン\t助動詞'))
        self.assertTrue(is_negative('ず\tズ\tズ\t助動詞'))
        self.assertTrue(is_negative('ナイ\tナイ\tナイ\t助動詞'))
        self.assertFalse(is_negative('て\tテ\tテ\t助動詞'))

class ISTaigigo(unittest.TestCase):
    def test_isTaigigo(self):
        self.assertTrue(is_Taigigo('大きい','小さい'))
        self.assertFalse(is_Taigigo('すごい','すごくない'))

if __name__ == '__main__':
    unittest.main()