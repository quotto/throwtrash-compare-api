from functools import lru_cache
from logging import getLogger,INFO,DEBUG,StreamHandler
logger = getLogger(__name__)
ch = StreamHandler()
ch.setLevel(DEBUG)
logger.addHandler(ch)
logger.setLevel(DEBUG)

@lru_cache(maxsize=4098)
def ld(s,t):
    '''
    レーベンシュタイン距離を算出する
    s=比較単語1,t=比較単語2
    '''
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

    # すべてのパターンで編集した中から最小の距離を返す
    return 1 + min(l1, l2, l3)

def get_distance(source, target):
    '''
    レーベンシュタイン距離に基づくスコアを返す
    source=入力単語
    target=比較対象になる単語
    '''

    # 得られた編集距離を単語の文字列長で除算する
    # 編集距離が文字列長に近いほどスコアは低くなる（類似性が低い）
    score = 1 - ld(source, target)/max(len(source), len(target))
    return score