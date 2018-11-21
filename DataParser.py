from bs4 import BeautifulSoup

class DataParser:

    def readData(self, filepath):
        fileoutput = open(str(filepath), "r+", encoding='utf8')
        allLines = fileoutput.read()

        return allLines
       # while fileoutput.readline() !=

    def parseData(self, content):
        xml = BeautifulSoup(content, features="xml")
        titles = xml.find_all('OrgQuestion')
        relquestion = ''
        for title in titles:
            print(title["ORGQ_ID"])
            print(title.OrgQSubject.get_text())
            print(title.OrgQBody.get_text())
            threads = title.find_all('Thread')
            for thread in threads:
                relquestionObj = thread.find('RelQuestion')
                print(relquestionObj['RELQ_ID'])

                relquestion = relquestionObj.get_text()

                relcomments = thread.find_all('RelComment')

                for relcomment in relcomments:
                    print(relcomment.get_text())
                print("relquestion ", relquestion)

                #print(thread["THREAD_SEQUENCE"])
                #print(thread.get_text())

        return "Sucess"