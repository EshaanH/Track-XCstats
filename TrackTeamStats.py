from bs4 import BeautifulSoup
import requests
import csv

def eventfunction (eventName, eventDistance):
        eventlist = list(timeList)
        indexstart = int(eventlist.index(eventName))
        currentvalue = 0
        while currentvalue < indexstart:
            eventlist.pop(0)
            currentvalue += 1
        
        indexend = int(eventlist.index('\xa0'))
        while len(eventlist) > indexend:
            eventlist.pop()        

        PRlist = list(eventlist)
        if "9" in PRlist:
            PRlist.remove("9")
        if "10" in PRlist:
            PRlist.remove("10")
        if "11" in PRlist:
            PRlist.remove("11")
        if "12" in PRlist:
            PRlist.remove("12")
        PRlist.remove(eventName)
        
        PRlist.sort()
        PRlist.insert(0, eventDistance + " PR:")

        while len(PRlist) > 2:
            PRlist.pop()

        for item in PRlist:
            personList.append(item)

url="https://www.athletic.net/TrackAndField/Report/FullSeasonTeam.aspx?SchoolID=1023&S=2022"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

nameList = ["dummy",]
for SeasonTables in doc.find_all('table', {"class" : "table table-responsive DataTable HLData seasonStats"}):
    atheleteName = SeasonTables.find('a')
    nameList.append(atheleteName.string)

nameList.remove("dummy")

for AtheleteTables in doc.find_all("div", {'class' : 'athlete showHistory d-flex flex-column flex-md-row'}):
    haveresults = AtheleteTables.find('table', {'class' : "DataTable HLData2 historyStats"})
    if len(str(haveresults))<10:
        NameTable = AtheleteTables.find("table", {'class': "table table-responsive DataTable HLData seasonStats"})
        atheleteName = NameTable.find('a')
        print("Removed: " + atheleteName.string + " (No Results)")
        nameList.remove(atheleteName.string)
        
file = open("DistanceTeamStats.csv", "w", newline="")
writer = csv.writer(file)

nameListIndex = 0
for historicalTables in doc.find_all('table', {'class' : "DataTable HLData2 historyStats"}):
    timeList = ["dummy"]

    for times in historicalTables.find_all('td'):
        timeList.append(times.string)
    
    timeList.remove("dummy")
    timeList.remove("Season Records")

    personList = [nameList[nameListIndex],]
    nameListIndex += 1
    shouldPrint = False

    while "2022 Outdoor" in timeList:
        timeList.remove('2022 Outdoor')
    while "2021 Outdoor" in timeList:
        timeList.remove('2021 Outdoor')
    while "2020 Outdoor" in timeList:
        timeList.remove('2020 Outdoor')
    while "2019 Outdoor" in timeList:
        timeList.remove('2019 Outdoor')
    
    if "800 Meters" in timeList:
        eventfunction("800 Meters", "800")
        shouldPrint = True

    if "1600 Meters" in timeList:
        eventfunction("1600 Meters", "1600")
        shouldPrint = True

    if "3200 Meters" in timeList:
        eventfunction("3200 Meters", "3200")
        shouldPrint = True

    if shouldPrint:
        writer.writerow(personList)

file.close