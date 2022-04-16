import csv
from bs4 import BeautifulSoup
import requests

url = "https://www.athletic.net/TrackAndField/Athlete.aspx?AID=14014172"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

file = open("TestResults.csv", "w", newline="")
writer = csv.writer(file)

skipcount=1
for seasonTables in  doc.find("div", {"class" : "col-md-7 pull-md-5 col-xl-8 pull-xl-4 col-print-7 athleteResults"}):

    for seasontable in seasonTables.find_all("div"):
        if skipcount == 1:
            seasongrade = seasontable.find("h5")
            splitlist = str(seasongrade).split('>')
            season1 = splitlist[1].split('<')[0]
            season = season1.strip()
            year = season.split()[0]
            grade1 = splitlist[-4]
            grade = grade1.split('<')[0]
            skipcount = 0
        else:
            skipcount =1 

        relevantTimeList = []
        shouldnext = True

        for titles in seasontable.find_all("h5"):
            if titles.string == "800 Meters":
                relevantTimeList.append("800 Meters")
            elif titles.string == "1600 Meters":
                relevantTimeList.append("1600 Meters")
            elif titles.string == "3200 Meters":
                relevantTimeList.append("3200 Meters")
            else:
                relevantTimeList.append("Meh.")            
            
        for item in relevantTimeList:
            if item == "800 Meters":
                shouldnext = False
            elif item == "1600 Meters":
                shouldnext = False
            elif item == "3200 Meters":
                shouldnext = False
        
        if shouldnext == True:
            continue
        
        timelistindex = 0
        for item in relevantTimeList:
            if item == "800 Meters":
                eventlistindex =-1
                for eventTimes in seasontable.find_all('table', {'class' : 'table table-sm table-responsive table-hover'}):
                    eventlistindex +=1
                    if eventlistindex != timelistindex:
                        continue

                    for time in eventTimes.find_all("tr"):
                        splitList = str(time).split('>')
                        realTime1 = splitList[15]
                        realTime2 = realTime1.split('<')[0]
                        meet = splitList[-6]
                        meet1 = meet.split('<')[0]
                        date = splitList[-9]
                        date1 = date.split('<')[0]
                        writer.writerow([year, date1, "800 Meters", realTime2, meet1, "Track", season, grade])

            elif item == "1600 Meters":
                eventlistindex =-1
                for eventTimes in seasontable.find_all('table', {'class' : 'table table-sm table-responsive table-hover'}):
                    eventlistindex +=1
                    if eventlistindex != timelistindex:
                        continue

                    for time in eventTimes.find_all("tr"):
                        splitList = str(time).split('>')
                        realTime1 = splitList[15]
                        realTime2 = realTime1.split('<')[0]
                        meet = splitList[-6]
                        meet1 = meet.split('<')[0]
                        date = splitList[-9]
                        date1 = date.split('<')[0]
                        writer.writerow([year, date1, "1600 Meters", realTime2, meet1, "Track", season, grade])
            elif item == "3200 Meters":
                eventlistindex =-1
                for eventTimes in seasontable.find_all('table', {'class' : 'table table-sm table-responsive table-hover'}):
                    eventlistindex +=1
                    if eventlistindex != timelistindex:
                        continue

                    for time in eventTimes.find_all("tr"):
                        splitList = str(time).split('>')
                        realTime1 = splitList[15]
                        realTime2 = realTime1.split('<')[0]
                        meet = splitList[-6]
                        meet1 = meet.split('<')[0]
                        date = splitList[-9]
                        date1 = date.split('<')[0]
                        writer.writerow([year, date1, "3200 Meters", realTime2, meet1, "Track", season, grade])
            timelistindex +=1
            
file.close