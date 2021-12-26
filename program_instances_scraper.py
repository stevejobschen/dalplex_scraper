from urllib.request import DataHandler, urlopen as uReq
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
        courseId = contentDictionary[i][9:45]
        semesterId = contentDictionary[i][57:93]
        f.write(i + ";" + courseId+";"+semesterId+";"+"\n")
    CsvWriterStop(f)

rootUrl = "https://www.dalsports.dal.ca/Program/GetProgramDetails?courseId=8993d840-c85b-4afb-b8a9-3c30b3c16817&semesterId=aba777e9-06a5-4d2b-a093-8ba8d8153881#"
uClient = uReq(rootUrl)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")
categorys = page_soup.findAll("div", {"class": "col-sm-6 col-md-4 program-schedule-card"})

linkDictionary = {}

for category in categorys:
    date = category.find("label", {"class": "program-schedule-card-header"}).get_text().strip()
    rawTimeSpots = category.find("small").get_text().strip()
    time = rawTimeSpots.split("\r")[0]
    spots = rawTimeSpots.split("\n")[2]
    link= category.find("a")['onclick']
    print(link)

    # linkDictionary.update({title.get_text():link.get('onclick').split("?",1)[1]})

#save to CSV
# CsvWriter(linkDictionary)