# import scikit learn and numpy libraries required for this code

import numpy as np
import os
from sklearn.feature_extraction.text import *
from sklearn.metrics.pairwise import cosine_similarity


class GVSM:
    corpus = []
    queryList = []

    def initi(self,comments: list, querys: list) -> str:
        global corpus
        global queryList
        queryList = querys
        corpus = comments

        print("Test")
        return "complete"

    def mainProcessLarge(self) -> str:


        tfidf_vectorizer = TfidfVectorizer(stop_words='english', min_df=0.08,
                                           use_idf=True)  # sklearn  function to make document vectors
        corpus_tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)  # scikit function to calculate tf-idf matrix

        corpus_tfidf_mat = corpus_tfidf_matrix.todense()  # matrix form of tf-idf matrix calculated above

        minterm = []  # list to store minterm unit vectors

        corpus_tfidf = np.array(corpus_tfidf_mat).tolist()
        #print("corpus_tfidf: ",str(corpus_tfidf))
        print(len(tfidf_vectorizer.vocabulary_))
        if (len(tfidf_vectorizer.vocabulary_) > 60):
            return "false"
        for key, value in sorted(tfidf_vectorizer.vocabulary_.items()):  # print the vocabulary of corpus
            print(key)

        print('--------------------------------------------------------------------------------------------')

        #Construct the minterms of GVSM vector space
        for i in corpus_tfidf:
            #print("i ",i)
            temp_l = i
            val = 0
            cn = 0

            for k in temp_l:
                if k > 0:
                    #print("cn ",cn)
                    #print("pow(2, cn): ",pow(2, cn))
                    val = val + pow(2, cn)
                    #val = 1
                cn = cn + 1
            #print("minterm: " + str(minterm))
            minterm = minterm + [val]
            #print("minterm: " + str(minterm))
        unit_vectors = []
        tot_words = len(tfidf_vectorizer.vocabulary_)

        p = []
        #size_of_minterms = pow(2, (tot_words))  # size of GVSM vector space is 2^total_words
        print("Calculate the index term vectors as linear combinations of minterm vectors")
        # Calculate the index term vectors as linear combinations of minterm vectors
        for i in range(0, tot_words):
           # tmp_unit_vector = np.zeros(pow(2, tot_words),np.dtype='float16')
            #tmp_unit_vector = np.zeros(pow(2, tot_words), dtype='float16')
            #tmp_unit_vector = [0] * pow(2, tot_words)
            print("filling array... ")
            print("tot_word  " + str(tot_words))
            tmp_unit_vector = np.zeros(pow(2, tot_words), np.float)
            #tmp_unit_vector = [0 for j in range(pow(2, tot_words))]
            #tmp_unit_vector = np.zeros(tot_words)
            cnt = 0
            #print("corpus_tfidf " + str(corpus_tfidf))
            #print("tmp_unit_vector " + str(tmp_unit_vector))
            for k in corpus_tfidf:
                cn = 0
                #print("K: "+ str(k))
                for l in k:
                    #print("L: " + str(l))
                    print("CNT: " + str(cnt))
                    if i == cn and l > 0:

                        #print("minterm[cnt]: " + str(minterm[cnt]))
                        tmp_unit_vector[minterm[cnt]] = tmp_unit_vector[minterm[cnt]] + l
                    cn = cn + 1
                cnt = cnt + 1

            magnitude = np.linalg.norm(tmp_unit_vector)
            myArr = np.array(tmp_unit_vector)
            newArr = myArr / magnitude
            p.append(newArr)

        queryVector = np.zeros(pow(2, tot_words))
        sim = []
        count_file = 0
        print("this loop constructs document and query vectors in the GVSM vector space as linear combination")
        # this loop constructs document and query vectors in the GVSM vector space as linear combination of minterm vectors and cosine similarity
        for doc in corpus_tfidf:

            docVector = np.zeros(pow(2, tot_words))
            count = 0  # keeps count of index terms

            for value in doc:
                docVector += (
                            value * p[count])  # product of tfidf value from matrix and nomrmalised term vectors from p
                count = count + 1

            if (count_file == 0):
                queryVector += docVector  # assign query vector



            cosine_similarity_matrix = np.vstack((queryVector, docVector))

            print("cosine_similarity_matrix " + str(cosine_similarity(cosine_similarity_matrix)))
            sim.append((cosine_similarity(cosine_similarity_matrix)[0][1],
                        os.path.basename(corpus[count_file])))  # cosine similarity

            count_file += 1
        # sort the documents based on their similarity from highest to lowest similarity order
        sim.sort(reverse=True)

        # print the documents' ranking
        for s in sim:
            print(s)

        return "success"
    def mainProcess(self) -> str:

        tfidf_vectorizer = TfidfVectorizer(stop_words='english', min_df=0.0,
                                           use_idf=True)  # scikit function to make document vectors

        corpus_tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)  # scikit function to calculate tf-idf matrix
        print("corpus_tfidf_matrix: " + str(corpus_tfidf_matrix.toarray()))
        tot_words = len(tfidf_vectorizer.vocabulary_)
        print('tot_words ' + str(tot_words))
        if(tot_words > 26):
            return "false"
        test = tfidf_vectorizer.transform(queryList)  # turn into document-term matrix (tf-idf)

        print("test: " + str(test.toarray()))
        test_qur = test.todense()
        print('tot_words query ' + str(len(tfidf_vectorizer.vocabulary_)))
        test_qur_list = np.array(test_qur).tolist()
        query_vector = [0 for j in range(pow(2, tot_words))]
        print("Query Vector "+query_vector)
        print('begin  corpus_tfidf_mat')
        corpus_tfidf_mat = corpus_tfidf_matrix.todense()  # matrix form of tf-idf matrix calculated above

        minterm = []  # list to store minterm unit vectors

        corpus_tfidf = np.array(corpus_tfidf_mat).tolist()

        print(len(tfidf_vectorizer.vocabulary_))

        for key, value in sorted(tfidf_vectorizer.vocabulary_.items()):  # print the vocabulary of corpus
            print(key)

        print('--------------------------------------------------------------------------------------------')

        # Construct the minterms of GVSM vector space
        for i in corpus_tfidf:

            temp_l = i
            val = 0
            cn = 0

            for k in temp_l:
                if k > 0:
                    val = val + pow(2, cn)
                cn = cn + 1
            minterm = minterm + [val]

        unit_vectors = []
        p = []
       #size_of_minterms = pow(2, (tot_words))  # size of GVSM vector space is 2^total_words

        # Calculate the index term vectors as linear combinations of minterm vectors
        for i in range(0, tot_words):
            tmp_unit_vector = [0 for j in range(pow(2, tot_words))]
            cnt = 0
            for k in corpus_tfidf:
                cn = 0
                for l in k:
                    if i == cn and l > 0:
                        tmp_unit_vector[minterm[cnt]] = tmp_unit_vector[minterm[cnt]] + l
                    cn = cn + 1
                cnt = cnt + 1
            magnitude = np.linalg.norm(tmp_unit_vector)
            myArr = np.array(tmp_unit_vector)
            newArr = myArr / magnitude
            p.append(newArr)

        query_vector = np.zeros(pow(2, tot_words))
        sim = []
        count_file = 0

        # loop constructs query vector from query doc in GVSM vector space as linear combination of minterm vectors
        for doc in test_qur_list:
            count = 0  # keeps count of index terms

            for value in doc:
                query_vector += (value * p[count])
                count = count + 1

        # this loop constructs document in the GVSM vector space as linear combination of minterm vectors and calculates cosine similarity
        for doc in corpus_tfidf:

            docVector = np.zeros(pow(2, tot_words))
            count = 0  # keeps count of index terms

            for value in doc:
                docVector += (
                            value * p[count])  # product of tfidf value from matrix and nomrmalised term vectors from p
                count = count + 1
            cosine_similarity_matrix = np.vstack((query_vector, docVector))

            print("cosine_similarity_matrix " + str(cosine_similarity(cosine_similarity_matrix)))
            sim.append((cosine_similarity(cosine_similarity_matrix)[0][1],
                        os.path.basename(corpus[count_file])))  # cosine similarity
            count_file += 1

        # sort the documents based on their similarity from highest to lowest similarity order
        sim.sort(reverse=True)

        # print the documents' ranking
        for s in sim:
            print(s)

        return "success"
