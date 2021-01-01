from app.word2vec import get_average_vector
import numpy as np
import unittest

class TestWord2Vec(unittest.TestCase):
    def test_get_average_vector_valid(self):
        vector_list = [
            np.array([1,2,3,4,5]),
            np.array([1,2,3,4,5]),
            np.array([1,2,3,4,5])
        ]
        feature_vector = get_average_vector(vector_list)
        self.assertEqual(feature_vector.shape[0],5)
        self.assertEqual(feature_vector[0],1)
        self.assertEqual(feature_vector[4],5)

if __name__ == "__main__":
    unittest.main()