from gensim import corpora
from gensim.summarization import bm25
from nltk.stem.porter import PorterStemmer

if __name__ == '__main__':

    p_stemmer = PorterStemmer()

    # 以下資料取自: https://www.businessinsider.com.au/bitcoin-futures-markets-unusual-behaviour-2018-2
    article_row=[
        'For the majority of bitcoin futures trading since their launch in December, the futures curves have been in steep contango, meaning that near-dated prices are below longer-dated prices,」 the analysts said',
        'But according to Goldman, the recent price action in Bitcoin futures implied higher prices for longer-dated contracts — far in excess of the cost to borrow money.',
        'Cboe futures contracts are also just based on one exchange — Gemini, run by the Winklevoss twins — whereas CME futures are based on a Bitcoin reference rate derived from an aggregate of major exchanges',
    ]

    article_list =[]
    for a in article_row:
        a_split = a.replace('?',' ').replace('(',' ').replace(')',' ').split(' ')
        # 詞干提取
        stemmed_tokens = [p_stemmer.stem(i) for i in a_split]
        article_list.append(stemmed_tokens)

    print("article_list " + str(article_list))
    query =['bitcoin','prices','futur','winklevoss']
    query_stemmed = [p_stemmer.stem(i) for i in query]
    print('query_stemmed :',query_stemmed )

    # bm25模型
    bm25Model = bm25.BM25(article_list)
    # 逆文件頻率
    average_idf = sum(map(lambda k: float(bm25Model.idf[k]), bm25Model.idf.keys())) / len(bm25Model.idf.keys())
    scores = bm25Model.get_scores(query_stemmed,average_idf)
    print('scores :',scores)