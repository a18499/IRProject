from bs4 import BeautifulSoup
from DataParser import DataParser as dp
from GVSM import GVSM as gs


if __name__ == '__main__':
  print("test")
  corpus = [
    'Preliminary Report-International Algebraic Language',
    'Extraction of Roots by Repeated Subtractions for Digital Computers',
    'Techniques Department on Matrix Program Schemes',
    'Two Square-Root Approximations'
  ]
  corpus.append("Kobe is a good player")
  q = ["Report-International test word","Report Matrix kobe"]
  print(gs.init(corpus,q))
  gs.mainProcess('test')

  '''content = dp.readData("datas/training_data/SemEval2016-Task3-CQA-QL-train-part2.xml")
  xml = BeautifulSoup(content, features="xml")
  titles = xml.find_all('OrgQuestion')
  for title in titles:
    print(title["ORGQ_ID"])
    print(title.OrgQSubject.get_text())
    print(title.OrgQBody.get_text())
    threads = title.find_all('Thread')
    for thread in threads:
        print(thread["THREAD_SEQUENCE"])
        print(thread.get_text())'''

