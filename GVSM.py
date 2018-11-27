# import scikit learn and numpy libraries required for this code

import numpy as np
import os
from sklearn.feature_extraction.text import *
from sklearn.metrics.pairwise import cosine_similarity
from gensim import corpora
from gensim.summarization import bm25
from nltk.stem.porter import PorterStemmer
import scipy.sparse as ss

class GVSM:
    corpus = []
    queryList = []

    def initi(self,comments: list, querys: list) -> str:
        global corpus
        global queryList
        queryList = querys
        corpus = comments


        return "complete"
    def testPM25(self):
        p_stemmer = PorterStemmer()


        article_row = [
            'For the majority of bitcoin futures trading since their launch in December, the futures curves have been in steep contango, meaning that near-dated prices are below longer-dated prices,」 the analysts said',
            'But according to Goldman, the recent price action in Bitcoin futures implied higher prices for longer-dated contracts — far in excess of the cost to borrow money.',
            'Cboe futures contracts are also just based on one exchange — Gemini, run by the Winklevoss twins — whereas CME futures are based on a Bitcoin reference rate derived from an aggregate of major exchanges',
        ]

        article_list = []
        #print("corpus " + str(corpus))
        #bagWord = CountVectorizer()
        #bagWord.fit_transform(corpus)
        #print("features " + str(bagWord.get_feature_names()))
        #tot_word = bagWord.get_feature_names()
        bagQuery = CountVectorizer()
        bagQuery.fit_transform(queryList)
        tot_query = bagQuery.get_feature_names()
        """for eachComment in corpus:
            bagWord = CountVectorizer()
            print("eachComment " + str(np.array(eachComment)))
            bagWord.fit_transform(np.array(eachComment))
            print("features " + str(bagWord.get_feature_names()))
            tot_word = bagWord.get_feature_names()
            article_list.append(tot_word)
        """
        for a in corpus:

            a_split = a.replace('?', ' ').replace('(', ' ').replace(')', ' ').split(' ')
            a = a.replace('\n', '')
            #print("a " + str([a]))
            if(a == "=("):
                article_list.append([a])
            elif(a == "."):
                article_list.append([a])
            elif(a == ":)"):
                article_list.append([a])
            elif (a == "!!"):
                article_list.append([a])
            else:
                #vectorizer = CountVectorizer(analyzer='word',token_pattern=u"(?u)\\b\\w*\\S*\\b")
                vectorizer = TfidfVectorizer(stop_words='english', min_df=0.08,token_pattern=u"\\b\\w*\\S*\\b",
                                           use_idf=True)
                X = vectorizer.fit_transform([a])
                stemmed_tokens = [p_stemmer.stem(i) for i in a_split]

                #print(" vectorizer.get_feature_names() " + str(vectorizer.get_feature_names()))
                article_list.append(vectorizer.get_feature_names())

        #print("article_list: " + str(article_list))
        #stemmed_tokens = [p_stemmer.stem(i) for i in tot_word]
        #article_list.append(stemmed_tokens)

        query = ['bitcoin', 'prices', 'futur', 'winklevoss']
        #print("queryList " + str(queryList))
        query_stemmed = [p_stemmer.stem(i) for i in tot_query]
        #print('query_stemmed :', query_stemmed)

        # bm25模型
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
    def myGVSM(self):
        vector = CountVectorizer()
        Document_Freuency = vector.fit_transform(corpus)
        feature_Name = vector.get_feature_names()
        tot_word = len(vector.get_feature_names())
        print("feature_Name: " + str(feature_Name))
        print("tot_word: " + str(tot_word))
        print("Document_Freuency: " + str(Document_Freuency.toarray()))

        mintermArray = []
        #Create minterm matrix
        print("Create minterm matrix... ")
        for i in Document_Freuency.toarray():
            #print("Each Doc " + str(np.array(i)))
            eachDocMinterm = np.zeros(tot_word)
            count = 0
            eachDoc = i
            for eachKeyWord in eachDoc:
                #print("eachKeyWord " + str(eachKeyWord))
                if(eachKeyWord > 0):
                    eachDocMinterm[count] = 1
                else:
                    eachDocMinterm[count] = 0
                count = count + 1
            #print("eachDocMinterm " + str(eachDocMinterm))
            mintermArray.append(eachDocMinterm)

        print("minterm array " + str(np.array(mintermArray)))
        print("minterm array size " + str(len(np.array(mintermArray))))
        document_num_to_minterm_num = dict()

        documentCount = 0
        #create document Index array calculate index
        for eachMintermValue in np.array(mintermArray):
            print("Each Minterm vaue " + str(eachMintermValue))
            square_num = 0
            value = 0
            for eachValue in eachMintermValue:
                #print("eachValue " + str(eachValue))
                if(eachValue > 0):
                    print("Square num " + str(square_num))
                    value = value + pow(2,square_num)
                square_num = square_num + 1
            document_num_to_minterm_num[documentCount] = value
            documentCount = documentCount + 1

        print(str(document_num_to_minterm_num))

        doccount = 0
        #calcuate conbination
        for eachDoc in Document_Freuency:
            #Check minterm whether is same or not

            doccount = doccount + 1

    def mainProcessLarge(self) -> str:


        tfidf_vectorizer = TfidfVectorizer(stop_words='english', min_df=0.08,
                                           use_idf=True)  # sklearn  function to make document vectors
        corpus_tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)  # scikit function to calculate tf-idf matrix

        print("corpus_tfidf_matrix: " + str(corpus_tfidf_matrix.toarray()))

        corpus_tfidf_mat = corpus_tfidf_matrix.todense()  # matrix form of tf-idf matrix calculated above

        minterm = []  # list to store minterm unit vectors

        corpus_tfidf = np.array(corpus_tfidf_mat).tolist()
        #print("corpus_tfidf: ",str(corpus_tfidf))
        print("Total word: " + str(len(tfidf_vectorizer.vocabulary_)))
        if (len(tfidf_vectorizer.vocabulary_) > 60):
            return "false"
        for key, value in sorted(tfidf_vectorizer.vocabulary_.items()):  # print the vocabulary of corpus
            print(key)

        print('--------------------------------------------------------------------------------------------')
        minterm_np = []
       # minterm_array = np.zeros(minterm_np)

        #Construct the minterms of GVSM vector space
        for i in corpus_tfidf:
            #print("i ",i)
            eachDoc = i
            val = 0
            cn = 0

            document_keyword_array = np.zeros(len(eachDoc))
            for keyword in eachDoc:

                if keyword > 0:

                    #print("pow(2, cn): ",pow(2, cn))
                    document_keyword_array[cn] = 1
                    val = val + pow(2, cn)
                    #val = 1
                else:
                    document_keyword_array[cn] = 0
                cn = cn + 1

            #print("minterm: " + str(minterm))
            print("document_keyword_array " + str(document_keyword_array))
            minterm_np.append(document_keyword_array)
            minterm = minterm + [val]
            print("minterm: " + str(minterm))
        unit_vectors = []

        print("minterm_np : " + str(np.array(minterm_np)))
        print("minterm_np length : " + str(len(np.array(minterm_np))))
        keywordVector = []
        #size_of_minterms = pow(2, (tot_words))  #size of GVSM vector space is 2^total_words
        print("Calculate the index term vectors as linear combinations of minterm vectors")
        # Calculate the index term vectors as linear combinations of minterm vectors
        tot_words = len(tfidf_vectorizer.vocabulary_)



        for i in range(0, tot_words):
           # tmp_unit_vector = np.zeros(pow(2, tot_words),np.dtype='float16')
            #tmp_unit_vector = np.zeros(pow(2, tot_words), dtype='float16')
            #tmp_unit_vector = [0] * pow(2, tot_words)

            print("filling array... ")
            print("tot_word  " + str(tot_words))
            tmp_unit_vector = np.zeros(pow(2, tot_words), dtype='uint8')

            #tmp_unit_vector = ss.lil_matrix((pow(2, tot_words), 0))
            #print("tmp_unit_vector " + str(tmp_unit_vector))
            #tmp_unit_vector = [0] * pow(2, tot_words)

            #tmp_unit_vector = [0 for j in range(pow(2, tot_words))]
            #tmp_unit_vector = np.zeros(tot_words)
            document_count = 0

            print("corpus_tfidf " + str(corpus_tfidf))
            print("corpus_tfidf len  " + str(len(corpus_tfidf)))
            #print("tmp_unit_vector " + str(tmp_unit_vector))
            for eachDoc in corpus_tfidf:
                eachKeyWordInDoc = 0
                print("eachDocument: " + str(eachDoc))
                print("eachDocument length: " + str(len(eachDoc)))
                for keyword in eachDoc:
                    #print("keyword: " + str(keyword))

                    #print("document_count: " + str(document_count))
                    if i == eachKeyWordInDoc and keyword > 0:

                        #print("minterm[document_count]: " + str(minterm[document_count]))
                        #tmp_unit_vector
                        tmp_unit_vector= tmp_unit_vector[minterm[document_count]] + keyword
                    eachKeyWordInDoc = eachKeyWordInDoc + 1
                document_count = document_count + 1

            magnitude = np.linalg.norm(tmp_unit_vector)
            myArr = np.array(tmp_unit_vector)
            newArr = myArr / magnitude
            keywordVector.append(newArr)
            print("keywordVector length: " + str(len(keywordVector)))

        queryVector = np.zeros(pow(2, tot_words))
        #queryVector =[0] * pow(2, tot_words)
        sim = []
        count_file = 0
        print("this loop constructs document and query vectors in the GVSM vector space as linear combination")
        # this loop constructs document and query vectors in the GVSM vector space as linear combination of minterm vectors and cosine similarity
        for doc in corpus_tfidf:

            docVector = np.zeros(pow(2, tot_words))
            #docVector = [0] * pow(2, tot_words)

            count = 0  # keeps count of index terms

            for value in doc:
                docVector += (
                            value * keywordVector[count])  # product of tfidf value from matrix and nomrmalised term vectors from p
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

        test = tfidf_vectorizer.transform(queryList)  # turn into document-term matrix (tf-idf)

        print("test: " + str(test.toarray()))
        test_qur = test.todense()
        print('tot_words query ' + str(len(tfidf_vectorizer.vocabulary_)))
        test_qur_list = np.array(test_qur).tolist()
        query_vector = [0 for j in range(pow(2, tot_words))]
        print("Query Vector "+ str(query_vector))
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
