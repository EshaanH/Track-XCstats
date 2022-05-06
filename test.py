import csv
from bs4 import BeautifulSoup
import requests
import timeconversion

url = "https://www.athletic.net/CrossCountry/Athlete.aspx?AID=11237593"

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
            if titles.string == "2 Miles":
                relevantTimeList.append("2 Miles")
            elif titles.string == "3 Miles":
                relevantTimeList.append("3 Miles")
            else:
                relevantTimeList.append("Meh.")            
            
        for item in relevantTimeList:
            if item == "2 Miles":
                shouldnext = False
            elif item == "3 Miles":
                shouldnext = False
        
        if shouldnext == True:
            continue
        
        timelistindex = 0
        for item in relevantTimeList:
            if item == "2 Miles":
                eventlistindex =-1
                for eventTimes in seasontable.find_all('table', {'class' : 'table table-sm table-responsive table-hover'}):
                    eventlistindex +=1
                    if eventlistindex != timelistindex:
                        continue

                    for time in eventTimes.find_all("tr"):
                        splitList = str(time).split('>')
                        realTime1 = splitList[17]
                        realTime2 = realTime1.split('<')[0]
                        meet = splitList[-4]
                        meet1 = meet.split('<')[0]
                        date = splitList[-7]
                        date1 = date.split('<')[0]
                        writer.writerow([year, date1, "2 Miles", realTime2, meet1, "XC", season, grade])

            elif item == "3 Miles":
                eventlistindex =-1
                for eventTimes in seasontable.find_all('table', {'class' : 'table table-sm table-responsive table-hover'}):
                    eventlistindex +=1
                    if eventlistindex != timelistindex:
                        continue

                    for time in eventTimes.find_all("tr"):
                        splitList = str(time).split('>')
                        realTime1 = splitList[17]
                        realTime2 = realTime1.split('<')[0]
                        meet = splitList[-4]
                        meet1 = meet.split('<')[0]
                        date = splitList[-7]
                        date1 = date.split('<')[0]
                        writer.writerow([year, date1, "3 Miles", realTime2, meet1, "XC", season, grade])
            
            timelistindex +=1
            
file.close