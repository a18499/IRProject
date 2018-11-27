from bs4 import BeautifulSoup
from DataParser import DataParser
from GVSM import GVSM
import threading
import numpy as np
def calculateJob(queryVector, docVector):
    gvsm = GVSM()
    gvsm.initi(docVector, queryVector)
    #gvsm.mainProcessLarge()
    #gvsm.mainProcess()
    #gvsm.myGVSM()
    result = gvsm.testPM25()
    #print("Result " + str(result))
    return result

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
  gvsm = GVSM()

  #print(own.initi(corpus, q))
  #own.mainProcess()
  #calculateJob(corpus, q)


  dataparser = DataParser()
  contents = dataparser.readData("datas/test_data/SemEval2017-task3-English-test-input.xml")

  relcommtents , relquests = dataparser.parseSubtaskAData(contents)

  for each_rel_request in relquests:
    #print("each_rel_request: " + str(each_rel_request.keys()))
    relQuestion = ""
    relQuestion_Content = ""
    for requestContent in each_rel_request:
      relQuestion = requestContent
      relQuestion_Content = each_rel_request[requestContent]
    for eachrelQuest in relcommtents.keys():
      if(eachrelQuest == relQuestion):
        #print("eachrelQuest: " + str(eachrelQuest))
        relcommtents_contents = relcommtents[eachrelQuest]
        #print("relcommtents_content " + str(relcommtents_contents))
        relcommentIDs = []
        relcommtentContents = []
        for eachrelcommentID in relcommtents_contents:
          #print("eachrelcommentID " + str(eachrelcommentID))
          relcommentIDs.append(eachrelcommentID)
          #print("eachrelcomment_Content " + str(relcommtents_contents[eachrelcommentID]))
          relcommtentContents.append(relcommtents_contents[eachrelcommentID])
        #print("input -------------------------")
        #print("relcommtents "+str(relcommtentContents))
        #print("relQuestion_Content "+str([relQuestion_Content]))
        results = calculateJob([relQuestion_Content], relcommtentContents)
        #print("result " + str(results))
        count = 0
        f = open("subtaskA.pred", "a")
        print("Result Size "+str(len(results)))
        for eachResult in results:
          print(str(eachrelQuest) +" "+ str(relcommentIDs[count]) + " 0 " + str(eachResult) + " false")
          f.write(str(eachrelQuest) +" "+ str(relcommentIDs[count]) + " 0 " + str(eachResult) + " false")
          f.write("\n")
          #print("Comment ID " + str(relcommentIDs[count]))
          #print("Score " + str(results[eachResult]))
          count = count + 1


  """allRelQuestion = dataparser.parseData(contents)

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
    result = calculateJob(query_vector, docVector)
    #t = threading.Thread(target= calculateJob(query_vector, docVector))
    #t.start()
    #threadPool.append(t)
"""
  #for eachThread in threadPool:
  #    print("wait for ", str(eachThread.getName()))
  #    eachThread.join()

