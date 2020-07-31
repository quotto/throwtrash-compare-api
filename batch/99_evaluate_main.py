import sys
import numpy as np
from logging import getLogger,INFO,DEBUG,FileHandler
from app.mecab_dict import is_Taigigo,is_negative,parse_from_standard_dict,parse_to_noun_from_custom_dict,reparse_text
from app.word2vec import get_vector,calculate_cosine_similarity,get_average_vector,calculate_word_similarity
from app.main import compare_two_text
import pandas as pd

logger = getLogger(__name__)
logger.setLevel(DEBUG)
fh = FileHandler("/app/dataset/evaluate/99.csv",mode="w",encoding="utf-8")
fh.setLevel(INFO)
logger.addHandler(fh)

df_data = pd.read_csv("/app/dataset/testdata.csv")

border_score = 0.6 #この数値以上なら一致、未満なら不一致

ok = 0 #正答数
diff = 0 #予測値との誤差
for row in df_data.itertuples():
    print(row)
    fh.terminator = ""
    logger.info("{0},{1}: predict={2},".format(row[1],row[2],row[3]))

    word1 = row[1]
    word2 = row[2]
    predict = int(row[3])

    result = compare_two_text(word1,word2)
    score = result['score']

    ans = 1 if(score >= border_score) else 0
    if(predict == ans):
        ok += 1
    diff += abs(predict - score)
    logger.info("score={0},diff={1}".format(score,abs(predict - score)))

    logger.info("\n")

logger.info("percent={0},diff_average={1}".format(ok/len(df_data),diff/len(df_data)))