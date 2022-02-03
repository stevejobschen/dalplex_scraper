from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import mariadb
import sys

def MariadbWriterInit():
    try:
        conn = mariadb.connect(
            user="testLocalUser",
            password="tLgkpKwjZR1.",
            host="192.168.0.27",
            port=3306,
            database="testLocalUser"
            )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn

def MariadbWriterClose(conn):
    conn.close


def CsvWriterStart(filename,headers):
    f = open(filename, "w")
    f.write(headers)
    return f

def CsvWriterClose(f):
    f.close

def CsvWriter(contentDictionary):
    f=CsvWriterStart("programs.csv","title;courseId;semesterId\n")
    for i in contentDictionary:
        courseId = contentDictionary[i][9:45]
        semesterId = contentDictionary[i][57:93]
        f.write(i + ";" + courseId+";"+semesterId+";"+"\n")
    CsvWriterClose(f)


def MariadbWriter(contentDictionary):
    conn = MariadbWriterInit()
    cur = conn.cursor()
    for i in contentDictionary:
        try:
            #cur.execute("INSERT INTO DalplexPrograms (title, courseID, semesterID) VALUES (?,?,?);",(i,contentDictionary[i][9:45],contentDictionary[i][57:93]))
            cur.execute("INSERT INTO DalplexPrograms (title, courseID, semesterID) VALUES (\'"+i+"\',\'"+contentDictionary[i][9:45]+"\',\'"+contentDictionary[i][57:93]+"\');")
        except mariadb.Error as e:
            print(f"Error: {e}")
    conn.commit()
    MariadbWriterClose(conn)

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
MariadbWriter(linkDictionary)
