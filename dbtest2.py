# Import libraries
import pandas as pd
import pymysql
from pymongo import MongoClient
import pymongo
from decimal import Decimal
import numpy as np
from datetime import datetime, timedelta


class datetimedays:
    def __init__(self):
        last_day_one = datetime.now() - timedelta(days=1)
        last_day_three = datetime.now() - timedelta(days=3)
        last_day_two = datetime.now() - timedelta(days=2)
        last_day_four = datetime.now() - timedelta(days=4)
        last_day_five = datetime.now() - timedelta(days=5)
        last_day_six = datetime.now() - timedelta(days=6)
        last_day_seven = datetime.now() - timedelta(days=7)
        last_day_eight = datetime.now() - timedelta(days=8)
        last_day_nine = datetime.now() - timedelta(days=9)
        last_day_ten = datetime.now() - timedelta(days=10)
        self.one_day_ago = last_day_one.strftime('%Y-%m-%d')
        self.two_days_ago = last_day_two.strftime('%Y-%m-%d')
        self.thre_days_ago = last_day_three.strftime('%Y-%m-%d')
        self.four_dyas_ago = last_day_four.strftime('%Y-%m-%d')
        self.fife_days_ago = last_day_five.strftime('%Y-%m-%d')
        self.six_days_ago = last_day_six.strftime('%Y-%m-%d')
        self.seven_days_ago = last_day_seven.strftime('%Y-%m-%d')
        self.eight_days_ago = last_day_eight.strftime('%Y-%m-%d')
        self.nine_days_ago = last_day_nine.strftime('%Y-%m-%d')
        self.ten_days_ago = last_day_ten.strftime('%Y-%m-%d')
        ################################# Mong db result ##################################
        # Connection to the MongoDB Server
        mongoClient = MongoClient("mongodb://localhost:27017")
        # Connection to the database
        db = mongoClient["petness"]
        # Collection
        collection = db["dog"]
        last_day = datetime.now() - timedelta(days=1)
        las = last_day.strftime('%Y-%m-%d')
        detailsrow = collection.find({'date': {"$regex": self.thre_days_ago}})
        detailsrow2 = collection.find({'date': {"$regex": self.two_days_ago}})
        krest = 0
        kstand = 0
        kruning = 0
        kwalking = 0
        for k in detailsrow:
            row = list(k.values())
            if row[3] == 3:
                # date1 = pd.date_range(row[0], periods=1, freq='T')
                # times = pd.DataFrame(index = date1)
                krest += 1
            if row[3] == 2:
                kruning += 1
            if row[3] == 1:
                kwalking += 1
            if row[3] == 0:
                kstand += 1
        self.restresult = krest
        self.runningresult = kruning
        self.walkingresult = kwalking
        self.standresult = kstand
        self.kdays()

#############################chosen k days ###################################################
    def kdays(self):
        # Connection to the MongoDB Server
        mongoClient = MongoClient("mongodb://localhost:27017")
        # Connection to the database
        db = mongoClient["petness"]
        # Collection
        collection = db["dog"]
        last_day = datetime.now() - timedelta(days=1)
        las = last_day.strftime('%Y-%m-%d')
        detailsrow = collection.find({'date': {"$regex": self.thre_days_ago}})
        detailsrow2 = collection.find({'date': {"$regex": self.two_days_ago}})
        krest = 0
        kstand = 0
        kruning = 0
        kwalking = 0
        for k in detailsrow:
            row = list(k.values())
            if row[3] == 3:
                # date1 = pd.date_range(row[0], periods=1, freq='T')
                # times = pd.DataFrame(index = date1)
                krest += 1
            if row[3] == 2:
                kruning += 1
            if row[3] == 1:
                kwalking += 1
            if row[3] == 0:
                kstand += 1

    ##################################### Wait to next midnoght ##################################

    def waitToNextMidnight(self):
        '''Wait to tomorrow 00:00 am.'''
        t = time.localtime()
        t = time.mktime(t[:3] + (0, 0, 0) + t[6:])
        time.sleep(t + 24 * 3600 - time.time())

#############################Insert Datebese###################################################

    def InsertDB(device_uuid, resting, staying, walking, running, health_status, date):
        conn = pymysql.connect(host='211.38.86.93',
                               user='root',
                               password='niceduri',
                               db='Pet-it',
                               charset='utf8')
        try:
            with conn.cursor() as cursor:
                #			sql = 'INSERT INTO behavior_log(uuid, resting, staying, walking, running, health_status, date TOKEN) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                #			cursor.execute(sql, (behavoir of pit action token_string))
                sql = 'INSERT INTO behavior_log (uuid, resting, staying, walking, running, health_status, date) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(sql, (device_uuid, resting, staying, walking, running, health_status, date))
                conn.commit()
                print(cursor.lastrowid)
        finally:
            conn.close()

        return cursor.lastrowid

#################################main function###################################################

    def main(self):
        print(self.restresult)
        print("\n")
        print(self.runningresult)

        # Run = float(run)/3600
        # time = pd.date_range(run, periods=2018, freq='5min')
        # series = pd.Series(np.random.randint(100, size=2018), index=time)
        # print(row)


if __name__ == '__main__':
    analyze = datetimedays()
    analyze.main()





