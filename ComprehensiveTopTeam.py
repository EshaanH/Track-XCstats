from bs4 import BeautifulSoup
import requests
import csv
import timeconversion

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
    
def getTopSchool(schoolid, fileName = "RelevantTeamTimes", XCtop2miles = 5, XCtop3miles = 10, TFtop3200 = 7, TFtop1600 = 7, TFtop800 = 5): #made this a function so it can be imported into other scripts and "schoolid" isn't forgotten    
    url = "https://www.athletic.net/CrossCountry/seasonbest?SchoolID=" + schoolid # XC Team Profile

    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    importantAtheleteList = []

    atheletenumber = 0
    for distance in doc.find_all("div", {'class': "distance"}): #this loops through all the distance tables in the html file
        eventName = str(distance.find('h3', {"class" : "mt-2"}))
        split1 = eventName.split('>',1)[1]
        split2 = split1.split('<',1)[0] #this turns the html of the event name into a string
        if split2 == "2 Miles":
            
            timeTable = distance.find('table', {'class': "table table-responsive DataTable"})
            for line in timeTable.find_all('tr'):
                
                link = str(line.find('a'))
                linksplit = link.split("\"",2)[1] #saves the athelete's link to bio, for future use
                
                importantAtheleteList.append(linksplit)
                
                atheletenumber += 1
                if atheletenumber == XCtop2miles: #stops the loop for running for every athelete and only pick the amount you choose when you call the function
                    break

        if split2 == "3 Miles":
            
            timeTable = distance.find('table', {'class': "table table-responsive DataTable"})
            atheletenumber=0
            
            for line in timeTable.find_all('tr'):
                
                link = str(line.find('a'))
                linksplit = link.split("\"",2)[1] #saves the athelete's link to bio, for future use
                importantAtheleteList.append(linksplit)
                
                atheletenumber += 1
                if atheletenumber == XCtop3miles: #stops the loop for running for every athelete and only pick the amount you choose when you call the function
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

    importantAtheleteList = templist #removes duplicates and does some additional filtering to track links
    
    templist = []
    for x in importantAtheleteList:
        if "meet" not in x:
            templist.append(x)

    importantAtheleteList = templist

    file_name = fileName + ".csv"
    file = open(file_name, "w", newline="") # creates the document in which the records are saved
    writer = csv.writer(file)

    for link in importantAtheleteList:
        XCurl = "https://www.athletic.net/CrossCountry/" + link
        TFurl = "https://www.athletic.net/TrackAndField/" + link
        XCgrade = ""
        TFgrade = ""
        gradeList = []

        result = requests.get(XCurl)
        doc = BeautifulSoup(result.text, "html.parser") # starts parsing the SC url

        title = str(doc.title.string)
        title = title.replace('\n','').replace('\t','').replace('\r','')
        athlete_name = title.split('-')[0] # gets the athelete name
        
        XCgrade  = doc.find('span', {'class' : 'float-right'})
        try:
            gradeList.append(XCgrade.string) # if there is a grade, it takes it
        except:
            XCgrade = "ZZZ"

        XCtwomiletime = ""
        XCthreemiletime = ""

        for event in doc.find_all('table', {"class" : "table table-sm histEvent"}): # goes to the PR table and gets their latest PRs
            for event_name in event.find_all('h5', {"class" : "bold"}):
                event_Name = (str(event_name.contents[0]))
                if event_Name == "2 Miles":
                    XCtwomiletime = bestTime(event)
                if event_Name == "3 Miles":
                    XCthreemiletime = bestTime(event)

        result = requests.get(TFurl)
        doc = BeautifulSoup(result.text, "html.parser")
        
        TFgrade  = doc.find('span', {'class' : 'float-right'})
        try:
            gradeList.append(TFgrade.string) # add the grade to the list
        except:
            XCgrade = "ZZZ"

        gradeList.sort()
        actualgrade=gradeList[-1] # sorts for the highest grade (ie. the last grade they ran XC or track)

        eighttime = ""
        sixtime = ""
        thirtytime = ""
        convertedeight = ""
        convertedthirty = ""

        for event in doc.find_all('table', {"class" : "table table-sm histEvent"}):
            for event_name in event.find_all('h5', {"class" : "bold"}):
                event_Name = (str(event_name.contents[0]))
                if event_Name == "800 Meters":
                    eighttime = bestTime(event)
                    convertedeight = timeconversion.convertTime800(eighttime)
                    eighttime = timeconversion.reformat(eighttime)
                if event_Name == "1600 Meters":
                    sixtime = bestTime(event)
                    sixtime = timeconversion.reformat(sixtime)
                if event_Name == "3200 Meters":
                    thirtytime = bestTime(event)
                    convertedthirty = timeconversion.convertTime3200(thirtytime)
                    thirtytime = timeconversion.reformat(thirtytime)

        templist = [convertedeight, sixtime, convertedthirty] #calculates their best estimated effort best event
        timesList = []
        for item in templist:
            if item != "":
                timesList.append(item)
        timesList.sort()

        timesList.append("")
        athleteStats = [athlete_name.strip(), link, actualgrade, XCtwomiletime, XCthreemiletime, eighttime, convertedeight, sixtime, thirtytime, convertedthirty, timesList[0]] # writes the header line for the person
        writer.writerow(athleteStats)
        writer.writerow("")
        writer.writerow(["Name of meet", "Season", "Year", "Date", "Race Distance", "Time", "XC/Track", "Grade"]) # starts their results table
   
        skipcount=1
        try: # some people have weird links or don't a season, so to avoid null pointer exceptions, if this errors out, it just assumes that the person has not run track
            for seasonTables in  doc.find("div", {"class" : "col-md-7 pull-md-5 col-xl-8 pull-xl-4 col-print-7 athleteResults"}):

                for seasontable in seasonTables.find_all("div"):
                    if skipcount == 1: # it only needs this data every other time, so it alternates pulling it and skipping it
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

                    for titles in seasontable.find_all("h5"): # it goes through all the events run in the season table. If there is a relevant event, it saves that information.
                        if titles.string == "800 Meters":
                            relevantTimeList.append("800 Meters")
                        elif titles.string == "1600 Meters":
                            relevantTimeList.append("1600 Meters") # this could just be one if statement with a bunch of "or"s, but for future expandability (maybe you only care about 32) its just gonna stay like this
                        elif titles.string == "3200 Meters":
                            relevantTimeList.append("3200 Meters")
                        else:
                            relevantTimeList.append("Meh.")            
                        
                    for item in relevantTimeList: # if there isn't a relevant event, "shouldnext" stays true and skips this year, cuz its not important
                        if item == "800 Meters":
                            shouldnext = False
                        elif item == "1600 Meters":
                            shouldnext = False
                        elif item == "3200 Meters":
                            shouldnext = False
                    
                    if shouldnext == True:
                        continue
                    
                    timelistindex = 0
                    for item in relevantTimeList: # loops through this list to know how much stuff it needs to pull
                        if item == "800 Meters": #checks what event it is, mostly to filter out non-distance events again, because its not needed
                            eventlistindex =-1
                            for eventTimes in seasontable.find_all('table', {'class' : 'table table-sm table-responsive table-hover'}):
                                eventlistindex +=1
                                if eventlistindex != timelistindex: # avoids duplicates???
                                    continue

                                for time in eventTimes.find_all("tr"): # pulls the data out of the line
                                    splitList = str(time).split('>')
                                    realTime1 = splitList[15]
                                    realTime2 = realTime1.split('<')[0]
                                    meet = splitList[-6]
                                    meet1 = meet.split('<')[0]
                                    date = splitList[-9]
                                    date1 = date.split('<')[0]
                                    writer.writerow([meet1, season, year, date1, "800 Meters", realTime2, "Track", grade]) #writes it into the line

                        elif item == "1600 Meters": # the event stuff is the same for each event so there isnt a need to explain again
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
                                    writer.writerow([meet1, season, year, date1, "1600 Meters", realTime2, "Track", grade])
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
                                    writer.writerow([meet1, season, year, date1, "3200 Meters", realTime2, "Track", grade])
                        timelistindex +=1
        except:
            print(athlete_name.strip() + " did not run track.") # the error, mentioned earlier

        result = requests.get(XCurl)
        doc = BeautifulSoup(result.text, "html.parser") #basically the same process as earlier just with XC

        skipcount=1
        try:    
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
                                    writer.writerow([meet1, season, year, date1, "2 Miles", realTime2, "XC", grade])

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
                                    writer.writerow([meet1, season, year, date1, "3 Miles", realTime2, "XC", grade])
                        
                        timelistindex +=1
        except:
            print(athlete_name.strip() + " did not run XC.")

        writer.writerow("") # adds a line of extra space between atheletes

    file.close

