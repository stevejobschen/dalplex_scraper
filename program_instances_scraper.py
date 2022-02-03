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

def CsvWriter(linksList):
    f=CsvWriterStart("programs_instance.csv","time;spots;link\n")
    for i in linksList:
        f.write(i["time"] + ";" + i["spots"]+";"+i["link"]+";"+"\n")
    CsvWriterClose(f)

def MariadbWriter(linksList):
    conn = MariadbWriterInit()
    cur = conn.cursor()
    for i in linksList:
        try:
            cur.execute("INSERT INTO DalplexProgramsInstances (time, spots) VALUES (\'"+i["time"]+"\',\'"+i["spots"]+"\');")
        except mariadb.Error as e:
            print(f"Error: {e}")
    conn.commit()
    MariadbWriterClose(conn)

rootUrl = "https://www.dalsports.dal.ca/Program/GetProgramDetails?courseId=8993d840-c85b-4afb-b8a9-3c30b3c16817&semesterId=aba777e9-06a5-4d2b-a093-8ba8d8153881#"
uClient = uReq(rootUrl)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")
categorys = page_soup.findAll("div", {"class": "col-sm-6 col-md-4 program-schedule-card"})

linksList = []

for category in categorys:
    date = category.find("label", {"class": "program-schedule-card-header"}).get_text().strip()
    rawTimeSpots = category.find("small").get_text().strip()
    time = rawTimeSpots.split("\r")[0]
    spots = rawTimeSpots.split("\n")[2]
    link= category.find("a")['onclick']

    print(link)

    tempDictionary = {"time":time,"spots":spots,"link":link}
    linksList.append(tempDictionary)

#save to CSV
CsvWriter(linksList)
MariadbWriter(linksList)
