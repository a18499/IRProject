#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import scikit learn and numpy libraries required for this code
import glob
import sys
import numpy as np
import os
from sklearn.feature_extraction.text import *
from sklearn.metrics.pairwise import cosine_similarity

if __name__ == '__main__':
	corpus = [
		'Preliminary Report-International Algebraic Language',
		'Extraction of Roots by Repeated Subtractions for Digital Computers',
		'Techniques Department on Matrix Program Schemes'
	]
	print('Enter the path of folder:')
	doc_path="datas/testGVSM/test_small/"
	files = glob.glob(doc_path)	#stores paths of all files as a list
	print('files')
	for file in files:
		print(str(file))

	tfidf_vectorizer = TfidfVectorizer('filename',stop_words='english',min_df=0.0,use_idf=True)	#scikit function to make document vectors

	vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
	transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
	tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵

	word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
	weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
	for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
		print("-------这里输出第", i, u"类文本的词语tf-idf权重------")
		for j in range(len(word)):
			print(word[j], weight[i][j])
	corpus_tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)#scikit function to calculate tf-idf matrix


	tot_words=len(vectorizer.vocabulary_)

	print('Enter the path of query document:')

	q=["Report-International test word", "test report"]
	query_vectorizer = CountVectorizer()
	test=query_vectorizer.fit_transform(q)#form the vector from query document
	query_word = query_vectorizer.vocabulary_  # 获取词袋模型中的所有词语
	print('query_word '+str(query_word))
	for key, value in sorted(query_vectorizer.vocabulary_.items()):  # print the vocabulary of corpus
		print(key)
	test_qur= test.todense()

	test_qur_list=np.array(test_qur).tolist()
	query_vector = [0 for j in range(pow(2,tot_words))]

	corpus_tfidf_mat=tfidf.todense()#matrix form of tf-idf matrix calculated above

	minterm=[]		#list to store minterm unit vectors

	corpus_tfidf=np.array(corpus_tfidf_mat).tolist()

	print(len(vectorizer.vocabulary_))


	for key,value in sorted(vectorizer.vocabulary_.items()):	#print the vocabulary of corpus
		print(key)

	print('--------------------------------------------------------------------------------------------')

	#Construct the minterms of GVSM vector space
	for i in corpus_tfidf:

		temp_l=i
		val=0
		cn=0

		for k in temp_l:
			if k > 0 :
				val=val+pow(2,cn)
			cn=cn+1
		minterm=minterm+[val]

	unit_vectors=[]
	p=[]
	size_of_minterms=pow(2,(tot_words))	#size of GVSM vector space is 2^total_words

	#Calculate the index term vectors as linear combinations of minterm vectors
	for i in range(0,tot_words):
		tmp_unit_vector = [0 for j in range(pow(2,tot_words))]
		cnt=0
		for k in corpus_tfidf:
			cn=0
			for l in k:
				if i == cn and l >0:
					tmp_unit_vector[minterm[cnt]]=tmp_unit_vector[minterm[cnt]]+l
				cn=cn+1
			cnt=cnt+1
		magnitude=np.linalg.norm(tmp_unit_vector)
		myArr=np.array(tmp_unit_vector)
		newArr=myArr/magnitude
		p.append(newArr)


	queryVector=np.zeros(pow(2,tot_words))
	sim=[]
	count_file=0

	#loop constructs query vector from query doc in GVSM vector space as linear combination of minterm vectors
	for doc in test_qur_list:
		count=0 #keeps count of index terms

		for value in doc:
			query_vector+=(value*p[count])
			count=count+1

	#this loop constructs document in the GVSM vector space as linear combination of minterm vectors and calculates cosine similarity
	for doc in corpus_tfidf:

		docVector=np.zeros(pow(2,tot_words))
		count=0 #keeps count of index terms

		for value in doc:
			docVector+=(value*p[count]) #product of tfidf value from matrix and nomrmalised term vectors from p
			count=count+1
		print("query_vector " + str(query_vector))
		print("docVector " + str(docVector))
		print("cosine_similarity "+str(cosine_similarity(query_vector,docVector)))
		sim.append((cosine_similarity(query_vector,docVector)[0][0],os.path.basename(corpus[count_file]))) #cosine similarity
		count_file+=1

	#sort the documents based on their similarity from highest to lowest similarity order
	sim.sort(reverse=True)

	#print the documents' ranking
	for s in sim:
		print(s)