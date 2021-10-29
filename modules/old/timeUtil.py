
from datetime import datetime

def getTimeNowAsNMEA():
    time = datetime.utcnow()
    nmeaTime = (time.hour * 10000) + (time.minute * 100) + (time.second)
    return nmeaTime

def getDateNowAsNMEA():
    date = datetime.utcnow()
    nmeaDate = (date.day * 10000) + (date.month * 100) + (date.year % 100)
    return nmeaDate