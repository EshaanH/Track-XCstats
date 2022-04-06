from bs4 import BeautifulSoup
import requests
import csv

#the reason these variables are declared like this is because maybe later they will passed in the python script as arguements
schoolid = "1023"
XCtop2miles = 5
XCtop3miles = 10
TFtop3200 = 7
TFtop1600 = 7
TFtop800 = 5

def bestTime(eventy):
    eventtimelist = ["Times:"]
    for times in eventy.find_all("a"):
        eventtimelist.append(times.string)
    currentValue = "NA"
    for input in eventtimelist:
        if "PR" in input:
            break
        elif "PR" not in input:
            currentValue = input
    return currentValue
    
url = "https://www.athletic.net/CrossCountry/seasonbest?SchoolID=" + schoolid # XC Team Profile

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

importantAtheleteList = []

atheletenumber = 0
for distance in doc.find_all("div", {'class': "distance"}):
    eventName = str(distance.find('h3', {"class" : "mt-2"}))
    split1 = eventName.split('>',1)[1]
    split2 = split1.split('<',1)[0]
    if split2 == "2 Miles":
        
        timeTable = distance.find('table', {'class': "table table-responsive DataTable"})
        for line in timeTable.find_all('tr'):
            
            link = str(line.find('a'))
            linksplit = link.split("\"",2)[1]
            
            importantAtheleteList.append(linksplit)
            atheletenumber += 1
            
            if atheletenumber == XCtop2miles:
                break

    if split2 == "3 Miles":
        
        timeTable = distance.find('table', {'class': "table table-responsive DataTable"})
        atheletenumber=0
        
        for line in timeTable.find_all('tr'):
            
            link = str(line.find('a'))
            linksplit = link.split("\"",2)[1]
            importantAtheleteList.append(linksplit)
            atheletenumber += 1
            
            if atheletenumber == XCtop3miles:
                break

url = "https://www.athletic.net/TrackAndField/EventRecords.aspx?SchoolID=" + schoolid # TF Team Profile
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

atheletenumber = 0
timeList = doc.find('table', {'class': "table table-responsive table-hover mt-1 DataTable"})
for line in timeList.find_all('tr'):
    if len(line) < 2:
        eventname = str(line.find('b'))
        if "800 Meters" in eventname:
            atheletenumber = TFtop800
        if "1600 Meters" in eventname:
            atheletenumber = TFtop1600
        if "3200 Meters" in eventname:
            atheletenumber = TFtop3200
    elif atheletenumber > 0:
        atheletenumber -= 1
        link = str(line.find('a'))
        linksplit = link.split("\"",2)[1]
        importantAtheleteList.append(linksplit)

templist = []
for x in importantAtheleteList:
    if x not in templist:
        templist.append(x)

importantAtheleteList = templist

file = open("TopOfTeam.csv", "w", newline="")
writer = csv.writer(file)
writer.writerow(["Name", "Grade", "XC 2 Mile", "XC 3 Mile", "800 Meters", "1600 Meters", "3200 Meters"]) #this gives each column a nice header when imported into google sheets. optional

for link in importantAtheleteList:
    XCurl = "https://www.athletic.net/CrossCountry/" + link
    TFurl = "https://www.athletic.net/TrackAndField/" + link
    trytrack = False
    
    result = requests.get(XCurl)
    doc = BeautifulSoup(result.text, "html.parser")

    title = str(doc.title.string)
    title = title.replace('\n','').replace('\t','').replace('\r','')
    athlete_name = title.split('-')[0]
    
    grade  = doc.find('span', {'class' : 'float-right'})
    try:
        testVar = grade.string
    except:
        tryTrack = True

    XCtwomiletime = ""
    XCthreemiletime = ""

    for event in doc.find_all('table', {"class" : "table table-sm histEvent"}):
        for event_name in event.find_all('h5', {"class" : "bold"}):
            event_Name = (str(event_name.contents[0]))
            if event_Name == "2 Miles":
                XCtwomiletime = bestTime(event)
            if event_Name == "3 Miles":
                XCthreemiletime = bestTime(event)

    result = requests.get(TFurl)
    doc = BeautifulSoup(result.text, "html.parser")
    
    if tryTrack:
        grade  = doc.find('span', {'class' : 'float-right'})

    eighttime = ""
    sixtime = ""
    thirtytime = ""

    for event in doc.find_all('table', {"class" : "table table-sm histEvent"}):
        for event_name in event.find_all('h5', {"class" : "bold"}):
            event_Name = (str(event_name.contents[0]))
            if event_Name == "800 Meters":
                eighttime = bestTime(event)
            if event_Name == "1600 Meters":
                sixtime = bestTime(event)
            if event_Name == "3200 Meters":
                thirtytime = bestTime(event)

    athleteStats = [athlete_name.strip(), grade.string, XCtwomiletime, XCthreemiletime, eighttime, sixtime, thirtytime]
    writer.writerow(athleteStats)
    
file.close