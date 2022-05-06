from bs4 import BeautifulSoup
import requests
import csv

url="https://www.athletic.net/CrossCountry/seasonbest?SchoolID=1023"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

eventList = ["Events:",]
for eventTables in doc.find_all('h3', {"class" : "mt-2"}):
    eventName = str(eventTables)

    split1 = eventName.split('>',1)[1]
    split2 = split1.split('<',1)[0]

    eventList.append(split2)
    print(split2)

eventList.remove("Events:")   
didjustindex = False
indexvalue = -1
for eventTimesTable in doc.find_all('table', {'class': "table table-responsive DataTable"}):    
    if didjustindex:
        didjustindex = False
    else:
        indexvalue += 1
        didjustindex = True
    currentEventName = eventList[indexvalue]
    for line in eventTimesTable.find_all('tr'):
        name = line.find('a')
        time = line.find_all('a')[1]
        grade = line.find_all('td')[1]
        atheleteStats = [name.string, time.string, grade.string, currentEventName,]
        print(atheleteStats)
        
    

        
