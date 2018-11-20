from bs4 import BeautifulSoup
from DataParser import DataParser as dp



if __name__ == '__main__':
  print("test")



  content = dp.readData("datas/training_data/SemEval2016-Task3-CQA-QL-train-part2.xml")
  xml = BeautifulSoup(content, features="xml")
  titles = xml.find_all('OrgQuestion')
  for title in titles:
    print(title["ORGQ_ID"])
    print(title.OrgQSubject.get_text())
    print(title.OrgQBody.get_text())
    threads = title.find_all('Thread')
    for thread in threads:
        print(thread["THREAD_SEQUENCE"])
        print(thread.get_text())

