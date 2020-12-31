import gensim
import sys
import numpy as np
from scipy import spatial
from logging import getLogger, DEBUG, StreamHandler
import os

logger = getLogger(__name__)
ch = StreamHandler()
ch.setLevel(DEBUG)
logger.addHandler(ch)
logger.setLevel(DEBUG)

ch.terminator = ''
logger.info("load word2vec models...")

model = gensim.models.word2vec.Word2Vec.load("{}/dataset/word2vec.gensim.model".format(os.path.dirname(__file__)))

ch.terminator = '\n'
logger.info("finish")
def get_vector(word):
    try:
        vector = model.wv[word]
        return vector
    except KeyError as err:
        print("key:"+word+"is not found")
        return np.array([])

def calculate_cosine_similarity(vec1,vec2):
    return 1 - spatial.distance.cosine(vec1,vec2)

def get_average_vector(vector_list):
    feature_vector = np.zeros((len(vector_list[0]),),dtype="float32")
    for vec in vector_list:
        feature_vector = np.add(feature_vector,vec)
    feature_vector = np.divide(feature_vector,len(vector_list))
    return feature_vector

def calculate_word_similarity(word1,word2):
    try:
        similarity = model.similarity(word1,word2)
        return similarity
    except KeyError as err:
       print(err) 
       return 0
