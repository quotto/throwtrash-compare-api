import falcon
import msgpack
from falcon import testing
import app.app as app
import unittest
from unittest.mock import MagicMock, patch

def client():
    return testing.TestClient(app.api)

class TestAPI(unittest.TestCase):
    def test_compare(self):
        response = client().simulate_get('/compare?word1=燃えるゴミ&word2=可燃ごみ')
        result_content = msgpack.unpackb(response.content,raw=False)
        self.assertEqual(response.status,falcon.HTTP_200)
        self.assertTrue(result_content['score']>0)
        self.assertEquals(result_content['match'],'可燃ごみ')

    def test_compare_multiple_target(self):
        # 比較対象（登録情報）が2つ以上ある場合
        response = client().simulate_get('/compare?word1=燃えるゴミ&word2=燃えないごみ可燃ごみ')
        result_content = msgpack.unpackb(response.content,raw=False)
        self.assertEqual(response.status,falcon.HTTP_200)
        self.assertTrue(result_content['score']>0)
        self.assertEquals(result_content['match'],'可燃ごみ')

    def test_compare_multiple_input_target(self):
        #入力と比較対象（登録情報）が2つ以上ある場合
        response = client().simulate_get('/compare?word1=ビンと可燃ごみ&word2=ビンカンペットボトル')
        result_content = msgpack.unpackb(response.content,raw=False)
        self.assertEqual(response.status,falcon.HTTP_200)
        self.assertTrue(result_content['score']>0)
        self.assertEquals(result_content['match'],'ビン')

    def test_compare_parameter_missing(self):
        #入力と比較対象（登録情報）が2つ以上ある場合
        response = client().simulate_get('/compare?word1=ビンと可燃ごみ')
        self.assertEqual(response.status,falcon.HTTP_400)

        response = client().simulate_get('/compare?word2=ビンと可燃ごみ')
        self.assertEqual(response.status,falcon.HTTP_400)

        response = client().simulate_get('/compare')
        self.assertEqual(response.status,falcon.HTTP_400)
    
    @patch('main.app.compare_two_text')
    def test_compare_unexpected_error(self,mock_compare):
        mock_compare.side_effect=Exception('Mock Exception')
        response = client().simulate_get('/compare?word1=ビンと可燃ごみ&word2=ビンカンペットボトル')
        self.assertEqual(response.status,falcon.HTTP_502)

if __name__ == '__main__':
    unittest.main()