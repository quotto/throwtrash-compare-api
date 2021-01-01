import MeCab
import pandas as pd
from logging import getLogger,INFO,DEBUG,StreamHandler
import os

logger = getLogger(__name__)
logger.setLevel(DEBUG)
ch = StreamHandler()
ch.setLevel(DEBUG)
logger.addHandler(ch)

ch.terminator = ''
logger.info("load user dict...")
customDict = MeCab.Tagger('-O chasen -u {}/dataset/user.dic'.format(os.path.dirname(__file__)))
ch.terminator = '\n'
logger.info("finish")

ch.terminator = ''
logger.info("load standard dict...")
standardDict = MeCab.Tagger('-O chasen')
ch.terminator = '\n'
logger.info("finish")


ch.terminator = ''
logger.info("load taigigo list...")
df_taigigo_tmp = pd.read_csv("{}/dataset/taigigo.csv".format(os.path.dirname(__file__)))
df_taigigo = pd.read_csv("{}/dataset/taigigo.csv".format(os.path.dirname(__file__)))
for index,rows in df_taigigo_tmp.iterrows():
    series = pd.Series([rows[1],rows[0]],index=df_taigigo.columns)
    df_taigigo = df_taigigo.append(series,ignore_index=True)

df_taigigo = df_taigigo.reset_index(drop=True)
ch.terminator = '\n'
logger.info("finish")

# パラメータword1とword2が登録された対義語であるか判定する
def is_Taigigo(word1,word2):
    s_taigigo = df_taigigo[df_taigigo['org'] == word1]
    result = len(s_taigigo) > 0 and s_taigigo['rev'].iat[0] == word2
    logger.debug('{0}⇔{1}は対義語？->{2}'.format(word1,word2,result))
    return result



# 与えられたMecabの分割結果からネガティブワード判定する
def is_negative(chasen):
    '''
    MecabのChasenフォーマットで分かち書きされたワード
    '''
    result = False

    logger.info(chasen)
    word = chasen.split('\t')

    # 品詞の特定
    word_type = word[3].split('-')

    # 品詞ごとにネガティブ判定する
    # 否定の否定があれば肯定とみなす
    if(word_type[0] == '名詞'):
        if(word[0][0] in ('非','不','無','未','反','異') or word[0] == '無い'):
            logger.debug('{0} is negative'.format(word[0]))
            result = True
    elif(word_type[0] == '助動詞'):
        if(word[0] in ('ない','ぬ','ん','ず','ナイ','ヌ','ン','ズ')):
            logger.debug('{0} is negative'.format(word[0]))
            result = True
    elif(word_type[0] == '形容詞'):
        if(word[0] in ('無い','ない')):
            logger.debug('{0} is negative'.format(word[0]))
            result = True
    return result

def parse_from_standard_dict(text):
    '''
    標準のIPADICによるMecabの分かち書き結果を返す
    text=対象文字列
    return 分かち書き結果のリスト（Chasenフォーマット）
    '''
    wordlist = standardDict.parse(text).split('\n')
    # 最後の2つはEOSとブランク
    result = []
    for word in wordlist[:len(wordlist)-2]:
        result.append(word)
    return result

def parse_to_noun_from_custom_dict(text):
    '''
    カスタム辞書からMecabによる分かち書きを行う
    text=対象ワード
    return word,reading,typeをキーに持つdict配列
    '''
    wordlist = customDict.parse(text).split('\n')
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
    '''
    Mecabによって分かち書きされた情報から名詞単位に統合する
    parse_list=Mecabの分かち書き結果をリスト化したもの,リストの要素はdict形式でword,reading,typeをキーにもつ
    '''
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