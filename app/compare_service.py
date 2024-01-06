from logging import getLogger,DEBUG,StreamHandler
import app.leven_shtein as leven_shtein
import app.mecab_dict as mecab_dict
import app.word2vec as word2vec

logger = getLogger(__name__)
logger.setLevel(DEBUG)
sh = StreamHandler()
sh.setLevel(DEBUG)
logger.addHandler(sh)

def scoring_by_distributed_expression(word1,word2):
    vector_bias1 = 0
    vector_bias2 = 0
    taigigo_bias = 0

    chasen = mecab_dict.parse_from_standard_dict(word1)
    logger.info(chasen)

    negative_dict1 = {}

    # 標準分かち書きの単位でベクトル取得 & ネガティブ判定
    for c in chasen:
        word_val = c.split('\t')[0]
        n_flg = mecab_dict.is_negative(c)
        if n_flg:
            vector_bias1 = 1  if(vector_bias1 == 0) else 0
        negative_dict1[word_val] = n_flg

    chasen2 = mecab_dict.parse_from_standard_dict(word2)
    logger.info(chasen2)

    negative_dict2 = {}
    for c in chasen2:
        word_val = c.split('\t')[0]
        n_flg = mecab_dict.is_negative(c)
        if n_flg:
            vector_bias2 = 1  if(vector_bias2 == 0) else 0
        negative_dict2[word_val] = n_flg

    count = 0
    total = 0
    for c1 in chasen:
        target1 = c1.split('\t')[0]
        word_type1 = c1.split('\t')[3].split('-')[0]
        for c2 in chasen2:
            target2 = c2.split('\t')[0]
            word_type2 = c2.split('\t')[3].split('-')[0]

            if(word_type1 == word_type2 and word_type1 in ('名詞', '形容詞') and
                mecab_dict.is_Taigigo(target1,target2)):
                # 対義語のバイアスは最大で2とする
                taigigo_bias = min(2,taigigo_bias+1)

            # 品詞が同じ場合に単語同士のコサイン類似度を求める
            if word_type1 == word_type2:
                val = word2vec.calculate_word_similarity(target1,target2)
                if val > 0:
                    count += 1
                    total += val

    bias = ((abs(vector_bias1 - vector_bias2)) + taigigo_bias)/3
    score = max(0,(total/count)-bias if(count>0) else 0)

    return score


def compare_two_text(text1,text2):
    logger.info("compare:%s,%s", text1, text2)
    wordlist1 = mecab_dict.reparse_text(mecab_dict.parse_to_noun_from_custom_dict(text1))
    wordlist2 = mecab_dict.reparse_text(mecab_dict.parse_to_noun_from_custom_dict(text2))

    logger.info("parsed:")
    logger.info(wordlist1)
    logger.info(wordlist2)

    max_score = 0
    similarity_word = ''
    for word1 in wordlist1:
        for word2 in wordlist2:
            logger.info("compare %s,%s", word1['word'], word2['word'])

            # 分散ベクトルによるスコアの算出
            score = scoring_by_distributed_expression(word1['word'], word2['word'])
            logger.info("de_score=%s", score)

            # 分散ベクトルでスコアが得られなければレーベンシュタイン距離を使う
            if score == 0:
                # レーベンシュタイン距離の算出
                score = leven_shtein.get_distance(word1['reading'], word2['reading'])
                logger.info('ld_score:%s', score)

            similarity_word = word2['word'] if score > max_score else similarity_word
            max_score = max(max_score, score)
    return {'match': similarity_word, 'score': max_score}
