import sys
import numpy as np
from logging import getLogger,INFO,DEBUG,FileHandler
from app.mecab_dict import is_Taigigo,is_negative,parse_from_standard_dict,parse_to_noun_from_custom_dict,reparse_text
from app.word2vec import get_vector,calculate_cosine_similarity,get_average_vector
import pandas as pd

logger = getLogger(__name__)
logger.setLevel(DEBUG)
fh = FileHandler("/app/dataset/evaluate/01.csv",mode="w",encoding="utf-8")
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

    vector_bias1 = 0
    vector_bias2 = 0
    taigigo_bias = 0

    print("parse to standard")
    chasen = parse_from_standard_dict(word1)
    print(chasen)

    vec_list = []
    negative_dict1 = {}

    # 標準分かち書きの単位でベクトル取得 & ネガティブ判定
    for c in chasen:
        word_val = c.split('\t')[0]
        vec_list.append(get_vector(word_val))
        n_flg = is_negative(c)
        if(n_flg): 
            vector_bias1 = 1  if(vector_bias1 == 0) else 0
        negative_dict1[word_val] = n_flg

    # 分散ベクトルの平均を算出
    feature_vec1 = get_average_vector(vec_list)

    print("parse to standard")
    chasen2 = parse_from_standard_dict(word2)
    print(chasen2)

    vec_list = []
    negative_dict2 = {}
    for c in chasen2:
        word_val = c.split('\t')[0]
        vec_list.append(get_vector(word_val))
        n_flg = is_negative(c)
        if(n_flg): 
            vector_bias2 = 1  if(vector_bias2 == 0) else 0
        negative_dict2[word_val] = n_flg
    feature_vec2 = get_average_vector(vec_list)

    print("taigigo check")
    for c1 in chasen:
        target1 = c1.split('\t')[0]
        word_type1 = c1.split('\t')[3].split('-')[0]
        vec1 = get_vector(target1)
        for c2 in chasen2: 
            target2 = c2.split('\t')[0]
            word_type2 = c2.split('\t')[3].split('-')[0]
            vec2 = get_vector(target2)

            if(word_type1 == word_type2 and word_type1 in ('名詞', '形容詞') and is_Taigigo(target1,target2)):
                # 対義語のバイアスは最大で2とする
                taigigo_bias = min(2,taigigo_bias+1)

    if(feature_vec1.size > 0 and feature_vec2.size > 0):
        similarity = calculate_cosine_similarity(feature_vec1,feature_vec2)
        bias = ((abs(vector_bias1 - vector_bias2)) + taigigo_bias)/3
        score = max(0,similarity-bias)

        ans = 1 if(score >= border_score) else 0
        if(predict == ans):
            ok += 1
        diff += abs(predict - score)
        logger.info("score={0},diff={1}".format(score,abs(predict - score)))
    logger.info("\n")

logger.info("percent={0},diff_average={1}".format(ok/len(df_data),diff/len(df_data)))
    

                