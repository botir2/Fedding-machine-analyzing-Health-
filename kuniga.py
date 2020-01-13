import datetime as dt
from threading import Timer
from pymongo import MongoClient
import pymongo
from decimal import Decimal
import numpy as np
from datetime import datetime, timedelta


###############weekdays time show function####################
last_day = datetime.now() - timedelta(days=1)
yest_day = datetime.now() - timedelta(days=2)

class kdays:
    def __init__(self):
        self.last_day_one = datetime.now() - timedelta(days=1)
        self.last_day_two = datetime.now() - timedelta(days=2)
        self.last_day_three = datetime.now() - timedelta(days=3)
        self.last_day_four = datetime.now() - timedelta(days=4)
        self.last_day_five = datetime.now() - timedelta(days=5)
        self.last_day_six = datetime.now() - timedelta(days=6)
        self.last_day_seven = datetime.now() - timedelta(days=7)
        self.last_day_eight = datetime.now() - timedelta(days=8)
        self.last_day_nine = datetime.now() - timedelta(days=9)
        self.last_day_ten = datetime.now() - timedelta(days=10)

#print (datetime.now())
#print date_N_days_ago

las=last_day.strftime('%Y-%m-%d')
yesterday=yest_day.strftime('%Y-%m-%d' )
print("Yesterday", las)

############################################################

def my_job():
    con = MongoClient('localhost', 27017)
    db=con.hayvon
    sogliq=db.sogliq
    a=[]
    k=db.sogliq.aggregate([
        {"$match" : {"Sana": {"$gt": yesterday, "$lte": las }}},
        {"$group" : {"_id":"$Activity", "count": {"$sum":1}}}
        ])

    for i in k:
        a=list(i.values())
    #prind(a)
        if a[1] == "Running":
            run = a[0]
        elif a[1] == "Resting":
            rest = a[0]
        elif a[1] == "Walking":
            walk = a[0]
        else:
            stand = a[0]
    Run=float(run)/3600

    Rest=float(rest)/3600

    Walk=float(walk)/3600

    Stand=float(stand)/3600
    fRun = open('running.txt', 'a')
    fRun.write(str(Run) + '  ')
    fRest = open('resting.txt', 'a')
    fRest.write(str(Rest) + '  ')
    fWalk = open('walking.txt', 'a')
    fWalk.write(str(Walk) + '  ')
    fStand = open('standing.txt', 'a')
    fStand.write(str(Stand) + '  ')
   
lastDay = dt.datetime.now() - dt.timedelta(days=1)
dateString = lastDay.strftime('%d-%m-%Y') + " 01-00-00"
newDate = lastDay.strptime(dateString,'%d-%m-%Y %H-%M-%S')
delay = (dt.datetime.now()-newDate).total_seconds()
Timer(delay,my_job,()).start()



