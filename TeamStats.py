from bs4 import BeautifulSoup
import requests
import csv

url="https://www.athletic.net/TrackAndField/Report/FullSeasonTeam.aspx?SchoolID=1023&S=2022"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

nameList = ["dummy",]
for SeasonTables in doc.find_all('table', {"class" : "table table-responsive DataTable HLData seasonStats"}):
    atheleteName = SeasonTables.find('a')
    nameList.append(atheleteName.string)

nameList.remove("dummy")
nameList.remove("Ved Joshi")
#print(nameList)

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
    
    shouldeight = False
    if "800 Meters" in timeList:
        eightlist = list(timeList)
        eightstart = int(eightlist.index("800 Meters"))
        currentvalue = 0
        while currentvalue < eightstart:
            eightlist.pop(0)
            currentvalue += 1
        
        eightend = int(eightlist.index('\xa0'))
        while len(eightlist) > eightend:
            eightlist.pop()        

        PRlist = list(eightlist)
        if "9" in PRlist:
            PRlist.remove("9")
        if "10" in PRlist:
            PRlist.remove("10")
        if "11" in PRlist:
            PRlist.remove("11")
        if "12" in PRlist:
            PRlist.remove("12")
        PRlist.remove('800 Meters')
        
        PRlist.sort()
        PRlist.insert(0, "800 PR:")

        while len(PRlist) > 2:
            PRlist.pop()

        for item in PRlist:
            personList.append(item)

        shouldPrint = True
        shouldeight = False

    shouldsix = False
    if "1600 Meters" in timeList:
        sixlist = list(timeList)
        sixstart = int(sixlist.index("1600 Meters"))
        currentvalue = 0
        while currentvalue < sixstart:
            sixlist.pop(0)
            currentvalue += 1
        
        sixend = int(sixlist.index('\xa0'))
        while len(sixlist) > sixend:
            sixlist.pop()

        PRlist = list(sixlist)
        if "9" in PRlist:
            PRlist.remove("9")
        if "10" in PRlist:
            PRlist.remove("10")
        if "11" in PRlist:
            PRlist.remove("11")
        if "12" in PRlist:
            PRlist.remove("12")
        PRlist.remove('1600 Meters')
        
        PRlist.sort()
        PRlist.insert(0, "1600 PR:")

        while len(PRlist) > 2:
            PRlist.pop()

        for item in PRlist:
            personList.append(item)

        shouldPrint = True
        shouldsix = True

    shouldthirty = False
    if "3200 Meters" in timeList:
        thirtylist = list(timeList)
        thirtystart = int(thirtylist.index("3200 Meters"))
        currentvalue = 0
        while currentvalue < thirtystart:
            thirtylist.pop(0)
            currentvalue += 1
        
        thirtyend = int(thirtylist.index('\xa0'))
        while len(thirtylist) > thirtyend:
            thirtylist.pop()

        PRlist = list(thirtylist)
        if "9" in PRlist:
            PRlist.remove("9")
        if "10" in PRlist:
            PRlist.remove("10")
        if "11" in PRlist:
            PRlist.remove("11")
        if "12" in PRlist:
            PRlist.remove("12")
        PRlist.remove('3200 Meters')
        
        PRlist.sort()
        PRlist.insert(0, "3200 PR:")

        while len(PRlist) > 2:
            PRlist.pop()

        for item in PRlist:
            personList.append(item)

        shouldPrint = True
        shouldthirty = True

    if shouldPrint:
        # if shouldeight:
        #     for item in eightlist:
        #         personList.append(item)
        # if shouldsix:
        #     for item in sixlist:
        #         personList.append(item)
        # if shouldthirty:
        #     for item in thirtylist:
        #         personList.append(item)
                
        writer.writerow(personList)

file.close
