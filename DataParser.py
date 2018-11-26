from bs4 import BeautifulSoup
import json
class DataParser:

    def readData(self, filepath):
        fileoutput = open(str(filepath), "r+", encoding='utf8')
        allLines = fileoutput.read()

        return allLines
       # while fileoutput.readline() !=

    def parseSubtaskAData(self, content):
        subtaskAdata = dict()
        recommtentsList = dict()
        relquests = []
        xml = BeautifulSoup(content, features="xml")
        titles = xml.find_all('OrgQuestion')
        for title in titles:
            print(title["ORGQ_ID"])
            print(title.OrgQSubject.get_text())
            print(title.OrgQBody.get_text())
            threads = title.find_all('Thread')
            relcomments = []
            for thread in threads:
                relquest_dic = dict()
                relquestionObj = thread.find('RelQuestion')
                print("RELQ_ID " + relquestionObj['RELQ_ID'])

                relquestion = relquestionObj.get_text()
                print("relquestion ", relquestion)
                relquest_dic[relquestionObj['RELQ_ID']] = relquestion
                relquests.append(relquest_dic)
                relcomments = thread.find_all('RelComment')
                relcommentDic = dict()
                for relcomment in relcomments:
                    print("RELC_ID: ", relcomment['RELC_ID'])
                    print("relcomment: ", relcomment.get_text())
                    relcommentDic[relcomment['RELC_ID']] = relcomment.get_text()
                    #relcommentList.append(relcomment.get_text())

                #dicts[relquestion] = relcommentDic
                recommtentsList[relquestionObj['RELQ_ID']] = relcommentDic
                # print(thread["THREAD_SEQUENCE"])
                # print(thread.get_text())
        return recommtentsList ,relquests
    def parseData(self, content):

        dicts = dict()
        relQuest_dict = dict()
        xml = BeautifulSoup(content, features="xml")
        titles = xml.find_all('OrgQuestion')
        relquestion = ''
        for title in titles:
            print(title["ORGQ_ID"])
            print(title.OrgQSubject.get_text())
            print(title.OrgQBody.get_text())
            threads = title.find_all('Thread')
            relcomments = []
            for thread in threads:
                relcomment_dic = dict()
                relquestionObj = thread.find('RelQuestion')
                print("RELQ_ID " + relquestionObj['RELQ_ID'])

                relquestion = relquestionObj.get_text()
                print("relquestion ", relquestion)

                relcomments = thread.find_all('RelComment')
                relcommentList = []
                for relcomment in relcomments:
                    print("RELC_ID: ", relcomment['RELC_ID'])
                    print("relcomment: ", relcomment.get_text())
                    relcommentList.append(relcomment.get_text())

                dicts[relquestion] = relcommentList
                #print(thread["THREAD_SEQUENCE"])
                #print(thread.get_text())

        return dicts