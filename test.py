import csv
from bs4 import BeautifulSoup
import requests
import timeconversion

def convertTime800(time, conversionFactor = 2.2):
    if "h" in time:
        time = time.replace("h","")
    secTime = 60 * int(time.split(":")[0]) + float(time.split(":")[1])
    convertedSec = secTime * conversionFactor
    min, sec = divmod(convertedSec, 60)
    return "%d:%02d" % (min, sec)

print(convertTime800("3:00h"))