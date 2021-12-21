from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def CsvWriterStart(filename,headers):
    f = open(filename, "w")
    f.write(headers)
    return f

def CsvWriterStop(f):
    f.close

def CsvWriter(contentDictionary):
    f=CsvWriterStart("programs.csv","title;courseId;semesterId\n")
    for i in contentDictionary:
        i
        courseId = contentDictionary[i][9:45]
        semesterId = contentDictionary[i][57:93]
        f.write(i + ";" + courseId+";"+semesterId+";"+"\n")
    CsvWriterStop(f)

