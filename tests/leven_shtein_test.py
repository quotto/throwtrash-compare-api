from app.leven_shtein import ld,get_distance
import unittest

class TestGetDistance(unittest.TestCase):
    def test_get_distance(self):
        score = get_distance('モエナイゴミ', 'モエルゴミ')
        self.assertEqual(score, 1-2/6)
        score = get_distance('あああああああ', 'いいいいいいいい')
        self.assertEqual(score, 0)

class TestLd(unittest.TestCase):
    def test_ld(self):
        score = ld('モエルゴミ','モエナイゴミ')
        self.assertEqual(score,2)

if __name__ == '__main__':
    unittest.main()
