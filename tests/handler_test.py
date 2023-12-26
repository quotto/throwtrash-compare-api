import base64
import msgpack
import app.handler as handler
import unittest
import json
from unittest.mock import MagicMock, patch

class TestAPI(unittest.TestCase):
    def test_compare(self):
        event = {
            'body':json.dumps({
                'target':'燃えるゴミ',
                'comparisons':['可燃ごみ']
            })
        }
        response = handler.lambda_handler(event,None)
        result_content = msgpack.unpackb(base64.b64decode(response['body']),raw=False)
        self.assertEqual(response['statusCode'],200)
        self.assertTrue(result_content[0]['score']>0)
        self.assertEquals(result_content[0]['match'],'可燃ごみ')

    def test_compare_multiple_comparison(self):
        # comparisonが複数指定されている場合は、各comparisonのスコアを返す

        event = {
            'body':json.dumps({
                'target':'燃えるゴミ',
                'comparisons':['可燃ごみ','燃えないごみ']
            })
        }
        response = handler.lambda_handler(event,None)
        result_content = msgpack.unpackb(base64.b64decode(response['body']),raw=False)
        self.assertEqual(response['statusCode'],200)
        self.assertEquals(len(result_content),2)
        self.assertTrue(result_content[0]['score']>0)
        self.assertEquals(result_content[0]['match'],'可燃ごみ')
        self.assertTrue(result_content[1]['score']>0)
        self.assertEquals(result_content[1]['match'],'燃えないごみ')
        # このテストデータの場合は、可燃ごみの方がスコアが高いはず
        self.assertTrue(result_content[0]['score']>result_content[1]['score'])

    def test_compare_multiple_target(self):
        # 一つの比較対象(comparison)に2つ以上の名詞が存在する場合は1番スコアの高いものを返す

        event = {
            'body':json.dumps({
                'target':'燃えるゴミ',
                'comparisons':['燃えないごみ可燃ごみ']
            })
        }
        response = handler.lambda_handler(event,None)
        result_content = msgpack.unpackb(base64.b64decode(response['body']),raw=False)
        self.assertEqual(response['statusCode'],200)
        self.assertTrue(result_content[0]['score']>0)
        self.assertEquals(result_content[0]['match'],'可燃ごみ')

    def test_compare_multiple_input_target(self):
        # 対象(target)と比較対象（comparison）それぞれに2つ以上の名詞が存在する場合は1番スコアの高いものを返す

        event = {
            'body':json.dumps({
                'target':'ビンと可燃ごみ',
                'comparisons':['ビンカンペットボトル']
            })
        }
        response = handler.lambda_handler(event,None)
        result_content = msgpack.unpackb(base64.b64decode(response['body']),raw=False)
        self.assertEqual(response['statusCode'],200)
        self.assertTrue(result_content[0]['score']>0)
        self.assertEquals(result_content[0]['match'],'ビン')

    def test_comparison_parameter_missing(self):
        # comparisonが指定されていない場合は400を返す

        event = {
            'body':json.dumps({
                'target':'ビンと可燃ごみ'
            })
        }
        response = handler.lambda_handler(event,None)
        self.assertEqual(response['statusCode'],400)

    def test_target_parameter_missing(self):
        # targetが指定されていない場合は400を返す

        event = {
            'body':json.dumps({
                'comparisons':['ビンと可燃ごみ']
            })
        }
        response = handler.lambda_handler(event,None)
        self.assertEqual(response['statusCode'],400)

        response = handler.lambda_handler({},None)
        self.assertEqual(response['statusCode'],400)

    # patchはインポートした側のモジュールから見たオブジェクトを指定する。
    # from app.compare_service import compare_two_textの場合はapp.handlerでcompare_two_textを参照しているので、
    # このような指定になる
    # 仮に import app.compare_service as compare_serviceとしていた場合は、patch('app.compare_service.compare_two_text')となる
    # https://docs.python.org/ja/3/library/unittest.mock.html#where-to-patch
    @patch('app.handler.compare_two_text')
    def test_compare_unexpected_error(self, mock_compare):
        mock_compare.side_effect=Exception('Mock Exception')

        event = {
            'body':json.dumps({
                'target':'ビンと可燃ごみ',
                'comparisons':['ビンカンペットボトル']
            })
        }
        response = handler.lambda_handler(event,None)
        self.assertEqual(response['statusCode'],502)

if __name__ == '__main__':
    unittest.main()