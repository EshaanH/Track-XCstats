def convertTime3200(time, conversionFactor = 2.15):
    secTime = 60 * int(time.split(":")[0]) + float(time.split(":")[1])
    convertedSec = secTime/conversionFactor
    min, sec = divmod(convertedSec, 60)
    return "%d:%02d" % (min, sec)

def convertTime800(time, conversionFactor = 2.2):
    secTime = 60 * int(time.split(":")[0]) + float(time.split(":")[1])
    convertedSec = secTime * conversionFactor
    min, sec = divmod(convertedSec, 60)
    return "%d:%02d" % (min, sec)

def format1600(time):
    return time.split(".")[0]


print(format1600("5:15.33"))

timeList = [convertTime800("2:19.03"),"5:15.33", convertTime3200("11:33.2")]
print(timeList)
timeList.sort()
print(timeList[0])
