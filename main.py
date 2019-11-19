import json
import os
import sys
import logging
from functools import lru_cache
sys.path.append(os.path.join(os.getcwd(),'package'))
import MeCab

mecab = MeCab.Tagger('-O chasen -d mecab-service/local/lib/mecab/dic/ipadic -u mecab-service/local/lib/mecab/dic/ipadic/user.dic')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

@lru_cache(maxsize=4098)
def ld(s,t):
    if not s: return len(t)
    if not t: return len(s)

    # 同じ位置の文字が同じなら次以降の文字列で比較
    if s[0] == t[0]: return ld(s[1:], t[1:])

    # 先頭に追加
    l1 = ld(s, t[1:])

    # 削除
    l2 = ld(s[1:], t)

    # 置換
    l3 = ld(s[1:], t[1:])

    return 1 + min(l1, l2, l3)

## source: 入力単語のカタカナリスト
## target: 比較対象になるカタカナリスト
def parse_ld(source, target):
    score_list = []
    # 1語ずつ編集距離の最良スコアを求める
    total = 0
    for s in source:
        max_score = 0
        for t in target:
            score = 1 - ld(s, t)/max(len(s), len(t))
            max_score = score if score > max_score else max_score
        total += max_score
    
    return round(total/len(source),2)
    
def parse_text(text):
    wordlist = mecab.parse(text).split('\n')
    result = []
    for word in wordlist[:len(wordlist)-2]:
        word_attr = word.split('\t')
        result.append(
            {
                'word': word_attr[0],
                'reading': word_attr[1],
                'type': word_attr[3].split('-')[0] #品詞は先頭のみ返す
            }
        )
    return result

def reparse_text(parse_list):
    tmp_word_list = []
    tmp_reading_list = []
    result = []
    for parse_text in parse_list:
        if(parse_text['type'] == '名詞'):
            result.append({
                'word': ''.join(tmp_word_list) + parse_text['word'],
                'reading': ''.join(tmp_reading_list) + parse_text['reading'],
                'type': '名詞'
            })
            tmp_word_list,tmp_reading_list = [],[]
        elif(parse_text['type'] in ['形容詞', '動詞', '助動詞', '連体詞']):
            tmp_word_list.append(parse_text['word'])
            tmp_reading_list.append(parse_text['reading'])

    return result

def compare_two_text(text1,text2):
    logging.info('compare:{},{}'.format(text1,text2))
    parse1 = reparse_text(parse_text(text1))
    parse2 = reparse_text(parse_text(text2))

    logging.info('parsed:')
    logging.info(parse1)
    logging.info(parse2)

    extract_lambda = lambda x: x['reading']
    score = parse_ld(list(map(extract_lambda,parse1)), list(map(extract_lambda,parse2)))
    logging.info('score:{}'.format(score))
    return score



def handler(event, context):
    logging.info("Received event: " + json.dumps(event, indent=2))
    resource = event['resource']
    result = {}
    if(resource == '/parse'):
        result = parse_text(event['queryStringParameters']['text'])
    elif(resource == '/compare'):
        queries = event['queryStringParameters']
        score = compare_two_text(queries['text1'],queries['text2'])
        result = {'score': score}
    else:
        return {
            'statusCode': 400,
            'headers': {'Content-type':'application/json'},
            'body': 'Invalid request'
        }

    return {
        'statusCode': 200,
        'headers': {'Content-type':'application/json'},
        'body': json.dumps(result)
    }

