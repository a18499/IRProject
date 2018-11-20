# import scikit learn and numpy libraries required for this code
import glob
import sys
import numpy as np
import os
from sklearn.feature_extraction.text import *
from sklearn.metrics.pairwise import cosine_similarity


class GVSM:
    copus = []
    queryList = []

    def init(comments: list, querys: list) -> str:
        global copus
        global queryList
        queryList = querys
        copus = comments

        print("Test")
        return "complete"

    def mainProcess(self) -> str:

        tfidf_vectorizer = TfidfVectorizer('filename', stop_words='english', min_df=0.0,
                                           use_idf=True)  # scikit function to make document vectors

        vectorizer = CountVectorizer()  # turn into term frequency matrix
        transformer = TfidfTransformer()  # calculate terms tf-idf weight

        return "success"
