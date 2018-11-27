from bs4 import BeautifulSoup

class DataParser:

    def readData(self, filepath):
        fileoutput = open(str(filepath), "r+", encoding='utf8')
        allLines = fileoutput.read()

        return allLines

    def parseSubtaskCData(self,content):
        xml = BeautifulSoup(content, features="xml")
        titles = xml.find_all('OrgQuestion')
        Orgquestion = dict()
        AllRelcomment = dict()
        for title in titles:
            print("ORGQ_ID: " + title["ORGQ_ID"])
            print("ORGQ_ID Content: " + title.OrgQSubject.get_text())
            threads = title.find_all('Thread')
            Orgquestion[ title["ORGQ_ID"]] = title.OrgQSubject.get_text()

            all_relcomment_list = []
            for thread in threads:
                relquestionObj = thread.find('RelQuestion')
                print("RELQ_ID " + relquestionObj['RELQ_ID'])
                relcomments = thread.find_all('RelComment')

                for relcomment in relcomments:
                    print("RELC_ID: ", relcomment['RELC_ID'])
                    print("relcomment: ", relcomment.get_text())
                    all_relcomment_list.append(relcomment.get_text())
                    AllRelcomment[relcomment['RELC_ID']] = relcomment.get_text()
            print("all_relcomment_list size: " + str(len(all_relcomment_list)))
            #AllRelcomment[title["ORGQ_ID"]] = all_relcomment_list
        return Orgquestion, AllRelcomment
    def parseSubtaskBData(self, content):
        xml = BeautifulSoup(content, features="xml")
        titles = xml.find_all('OrgQuestion')
        Orgquestion = dict()
        RelQuestion = dict()
        for title in titles:
            print("ORGQ_ID: " + title["ORGQ_ID"])
            print("ORGQ_ID Content: " + title.OrgQSubject.get_text())
            Orgquestion[title["ORGQ_ID"]] = title.OrgQSubject.get_text()
            threads = title.find_all('Thread')
            for thread in threads:
                relquestionObj = thread.find('RelQuestion')
                print("RELQ_ID: " + relquestionObj['RELQ_ID'])
                print("RELQ_Content: " + relquestionObj.RelQSubject.get_text())
                RelQuestion[relquestionObj["RELQ_ID"]] = relquestionObj.RelQSubject.get_text()

        return Orgquestion, RelQuestion

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