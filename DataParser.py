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

            threads = title.find_all('Thread')
            Orgquestion[ title["ORGQ_ID"]] = title.OrgQSubject.get_text()

            all_relcomment_list = []
            for thread in threads:
                relquestionObj = thread.find('RelQuestion')

                relcomments = thread.find_all('RelComment')

                for relcomment in relcomments:

                    all_relcomment_list.append(relcomment.get_text())
                    AllRelcomment[relcomment['RELC_ID']] = relcomment.get_text()

            #AllRelcomment[title["ORGQ_ID"]] = all_relcomment_list
        return Orgquestion, AllRelcomment
    def parseSubtaskBData(self, content):
        xml = BeautifulSoup(content, features="xml")
        titles = xml.find_all('OrgQuestion')
        Orgquestion = dict()
        RelQuestion = dict()
        for title in titles:

            Orgquestion[title["ORGQ_ID"]] = title.OrgQSubject.get_text()
            threads = title.find_all('Thread')
            for thread in threads:
                relquestionObj = thread.find('RelQuestion')
                RelQuestion[relquestionObj["RELQ_ID"]] = relquestionObj.RelQSubject.get_text()

        return Orgquestion, RelQuestion

    def parseSubtaskAData(self, content):

        recommtentsList = dict()
        relquests = []
        xml = BeautifulSoup(content, features="xml")
        titles = xml.find_all('OrgQuestion')
        for title in titles:

            threads = title.find_all('Thread')

            for thread in threads:
                relquest_dic = dict()
                relquestionObj = thread.find('RelQuestion')

                relquestion = relquestionObj.get_text()
                relquest_dic[relquestionObj['RELQ_ID']] = relquestion
                relquests.append(relquest_dic)
                relcomments = thread.find_all('RelComment')
                relcommentDic = dict()
                for relcomment in relcomments:

                    relcommentDic[relcomment['RELC_ID']] = relcomment.get_text()

                recommtentsList[relquestionObj['RELQ_ID']] = relcommentDic


        return recommtentsList ,relquests
