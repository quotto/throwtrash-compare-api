import json
import os
import sys
sys.path.append(os.path.join(os.getcwd(),'package'))
import MeCab

def handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    mecab = MeCab.Tagger('-O chasen -d mecab-service/local/lib/mecab/dic/ipadic -u mecab-service/local/lib/mecab/dic/ipadic/user.dic')
    wordlist = mecab.parse(event['queryStringParameters']['text']).split('\n')
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
    return {
        'statusCode': 200,
        'headers': {'Content-type':'application/json'},
        'body': json.dumps(result)
    }

