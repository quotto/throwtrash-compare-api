import sys,os
import unittest
import json
from main import handler

class TestMain(unittest.TestCase):
    def test_single_noun(self):
        result = handler({'queryStringParameters': {'text':'東京'}},{})
        response_body = json.loads(result['body'])
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(len(response_body),1)
        self.assertEqual(response_body[0]['word'],'東京')
        self.assertEqual(response_body[0]['reading'],'トウキョウ')
        self.assertEqual(response_body[0]['type'],'名詞')

    def test_multiple_noun(self):
        result = handler({'queryStringParameters':{'text': '東京スカイツリー'}},{})
        response_body = json.loads(result['body'])
        self.assertEqual(len(response_body),3)
        
    def test_text(self):
        result = handler({'queryStringParameters': {'text': 'プラスチックと燃えるゴミ'}},{})
        response_body = json.loads(result['body'])
        self.assertEqual(len(response_body),4)
        self.assertEqual(response_body[1]['type'], '助詞')
        self.assertEqual(response_body[2]['type'], '動詞')

if __name__ == '__main__':
    unittest.main()