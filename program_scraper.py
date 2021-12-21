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

rootUrl = "https://www.dalsports.dal.ca/Program/GetProducts?classification=f22e8568-5cb8-464f-93f6-b390759240de"
uClient = uReq(rootUrl)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")
categorys = page_soup.findAll("div", {"class": "list-group-item"})

linkDictionary = {}

for category in categorys:
    link = category.find("div", {"class": "row"})
    title = category.find("h3", {"class": "TitleText-SP"})
    linkDictionary.update({title.get_text():link.get('onclick').split("?",1)[1]})

#save to CSV
CsvWriter(linkDictionary)
