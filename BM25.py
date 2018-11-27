from sklearn.feature_extraction.text import *

from gensim.summarization import bm25
from nltk.stem.porter import PorterStemmer


class BM25:
    corpus = []
    queryList = []

    def init_param(self, comments: list, querys: list) -> str:
        global corpus
        global queryList
        queryList = querys
        corpus = comments
        return "complete"

    def mainprocess(self):
        p_stemmer = PorterStemmer()

        article_list = []

        # spilt sentence into token
        bagQuery = CountVectorizer()
        bagQuery.fit_transform(queryList)
        tot_query = bagQuery.get_feature_names()

        for a in corpus:

            # a_split = a.replace('?', ' ').replace('(', ' ').replace(')', ' ').split(' ')
            a = a.replace('\n', '')
            # handle some special case
            if a == "=(":
                article_list.append([a])
            elif a == ".":
                article_list.append([a])
            elif a == ":)":
                article_list.append([a])
            elif a == "!!":
                article_list.append([a])
            else:

                vectorizer = TfidfVectorizer(stop_words='english', min_df=0.08, token_pattern=u"\\b\\w*\\S*\\b",
                                             use_idf=True)
                vectorizer.fit_transform([a])
                article_list.append(vectorizer.get_feature_names())



        query_stemmed = [p_stemmer.stem(i) for i in tot_query]

        # bm25 model
        bm25Model = bm25.BM25(article_list)
        # tf-idf
        average_idf = sum(map(lambda k: float(bm25Model.idf[k]), bm25Model.idf.keys())) / len(bm25Model.idf.keys())
        scores = bm25Model.get_scores(query_stemmed, average_idf)
        print('scores :', scores)

        count = 0
        result = dict()

        for eachScore in scores:
            result[corpus[count]] = eachScore
            count = count + 1
        print("result " + str(result))
        return scores
