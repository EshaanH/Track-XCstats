from bs4 import BeautifulSoup
import requests
import csv

with open('AtheleteLinks.csv', mode ='r')as file:

    linksFile = csv.reader(file)

    urlList = ["dummy",]
    numLines = 0
    
    for lines in linksFile:
            for links in lines:
                urlList.append(links)
            numLines += 1

urlList.remove("dummy")
while numLines > 1:
    urlList.remove('')
    numLines -= 1

file = open("AtheleteStats.csv", "w", newline="")
writer = csv.writer(file)

for url in urlList:
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    title = str(doc.title.string)
    title = title.replace('\n','').replace('\t','').replace('\r','')
    athlete_name = title.split('-')[0]

    athleteStats = [athlete_name.strip(),]
    
    school = doc.find_all("b")[1]
    athleteStats.append(school.string)

    for event in doc.find_all('table', {"class" : "table table-sm histEvent"}):
        for event_name in event.find_all('h5', {"class" : "bold"}):
            eventName = (str(event_name.contents[0]))
            athleteStats.append(eventName)
        
        eventTimeList = ["Times:",]
        for times in event.find_all("a"):
            eventTimeList.append(times.string)
        currentValue = "NA"
        for input in eventTimeList:
            if "PR" in input:
                break
            elif "PR" not in input:
                currentValue = input
        athleteStats.append(currentValue)
                
    writer.writerow(athleteStats)
    #print(athleteStats)

file.close