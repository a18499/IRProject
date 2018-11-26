from bs4 import BeautifulSoup
from DataParser import DataParser
from GVSM import GVSM
import threading

def calculateJob(queryVector, docVector):
    gvsm = GVSM()
    gvsm.initi(docVector, queryVector)
    #gvsm.mainProcessLarge()
    gvsm.myGVSM()
if __name__ == '__main__':
  print("test")
  corpus = [
    'Report-International kobe word',
    'Preliminary Report-International Algebraic Language',
    'Extraction of Roots by Repeated Subtractions for Digital Computers',
    'Techniques Department on Matrix Program Schemes',
    'Two Square-Root Approximations'
  ]
  corpus.append("Kobe is a good player")
  q = ["Report-International kobe word"]
  #gvsm = GVSM()

  #print(own.initi(corpus, q))
  #own.mainProcess()

  dataparser = DataParser()
  contents = dataparser.readData("datas/training_data/SemEval2016-Task3-CQA-QL-train-part2.xml")
  allRelQuestion = dataparser.parseData(contents)
  print(allRelQuestion.keys())
  threadPool = []
  for eachKey in allRelQuestion:
    print("Question: ",eachKey)
    query_vector = []
    query_vector.append(eachKey)

    allComment = allRelQuestion[eachKey]
    print("allComment: ", str(allComment))
    print("allComment size: ", len(allComment))
    docVector = allComment
    #gvsm.initi(docVector, query_vector)
    #gvsm.mainProcess()
    large = query_vector + docVector
    calculateJob(query_vector, large)
    #t = threading.Thread(target= calculateJob(query_vector, docVector))
    #t.start()
    #threadPool.append(t)

  #for eachThread in threadPool:
  #    print("wait for ", str(eachThread.getName()))
  #    eachThread.join()

