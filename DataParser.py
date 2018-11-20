class DataParser:

    def readData(filepath):
        fileoutput = open(str(filepath), "r+", encoding='utf8')
        allLines = fileoutput.read()

        return allLines
       # while fileoutput.readline() !=