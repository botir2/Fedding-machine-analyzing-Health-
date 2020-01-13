# Import libraries
import pandas as pd
import pymysql
from pip._vendor.distlib.compat import raw_input
from pymongo import MongoClient
import pymongo
from decimal import Decimal
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from time import sleep
from threading import Thread
from itopen import hlbad, hlgood, hlwarming, t1


class datetimedays(Thread):
    def __init__(self, choselist):
        super(datetimedays, self).__init__()
        self.choselist = choselist
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
        self.three_days_ago = last_day_three.strftime('%Y-%m-%d')
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
        self.db = db
        # Collection
        collection = db["dog"]
        self.collection = collection
        # server.stop()

        today = datetime.now().strftime("%Y-%m-%d %H:%M")

    #######################################main function###################################################
    def run(self):
        detailsrow1 = self.collection.find({'date': {"$regex": self.one_day_ago}})
        detailsrow2 = self.collection.find({'date': {"$regex": self.two_days_ago}})
        detailsrow3 = self.collection.find({'date': {"$regex": self.three_days_ago}})
        detailsrow4 = self.collection.find({'date': {"$regex": self.four_dyas_ago}})
        detailsrow5 = self.collection.find({'date': {"$regex": self.fife_days_ago}})
        detailsrow6 = self.collection.find({'date': {"$regex": self.six_days_ago}})
        detailsrow7 = self.collection.find({'date': {"$regex": self.seven_days_ago}})
        detailsrow8 = self.collection.find({'date': {"$regex": self.eight_days_ago}})
        detailsrow9 = self.collection.find({'date': {"$regex": self.nine_days_ago}})
        detailsrow10 = self.collection.find({'date': {"$regex": self.ten_days_ago}})

        df = pd.DataFrame(list(detailsrow1))  # one day ago
        df2 = pd.DataFrame(list(detailsrow2))
        df3 = pd.DataFrame(list(detailsrow3))
        df4 = pd.DataFrame(list(detailsrow4))
        df5 = pd.DataFrame(list(detailsrow5))
        df6 = pd.DataFrame(list(detailsrow6))
        df7 = pd.DataFrame(list(detailsrow7))
        df8 = pd.DataFrame(list(detailsrow8))
        df9 = pd.DataFrame(list(detailsrow9))
        df10 = pd.DataFrame(list(detailsrow10))

        try:
            g = df.groupby("activity")  # one day ago
        except:
            g = 0
        try:
            g2 = df2.groupby("activity")
        except:
            g2 = 0
        try:
            g3 = df3.groupby("activity")
        except:
            g3 = 0
        try:
            g4 = df4.groupby("activity")  # one day ago
        except:
            g4 = 0
        try:
            g5 = df5.groupby("activity")
        except:
            g5 = 0
        try:
            g6 = df6.groupby("activity")
        except:
            g6 = 0
        try:
            g7 = df7.groupby("activity")  # one day ago
        except:
            g7 = 0
        try:
            g8 = df8.groupby("activity")
        except:
            g8 = 0
        try:
            g9 = df9.groupby("activity")
        except:
            g9 = 0
        try:
            g10 = df10.groupby("activity")  # do it till the end
        except:
            g10 = 0

        # print(g9)

        ###################### day 1 count action ##############
        try:
            krest = g.get_group(3).count() * 5 / 60  # get activity belog to 0,1,2,3
        except:
            krest = 0
        try:
            kstand = g.get_group(2).count() * 5 / 60  # get activity belog to 0,1,2,3
        except:
            kstand = 0
        try:
            kruning = g.get_group(0).count() * 5 / 60  # get activity belog to 0,1,2,3
        except:
            kruning = 0
        try:
            kwalking = g.get_group(1).count() * 5 / 60  # get activity belog to 0,1,2,3
        except:
            kwalking = 0

        ###################### day 2 count action ################
        try:
            kresttwo = g2.get_group(3).count() * 5 / 60  # get activity belog to 0,1,2,3
        except:
            kresttwo = 0
        try:
            kstandtwo = g2.get_group(2).count() * 5 / 60  # get activity belog to 0,1,2,3
        except:
            kstandtwo = 0
        try:
            kruningtwo = g2.get_group(0).count() * 5 / 60  # get activity belog to 0,1,2,3
        except:
            kruningtwo = 0
        try:
            kwalkingtwo = g2.get_group(1).count() * 5 / 60  # get activity belog to 0,1,2,3
        except:
            kwalkingtwo = 0

        ################### day 3 count action ###################
        try:
            krestthree = g3.get_group(3).count() * 5 / 60  # get activity belog to 0,1,2,3
        except:
            krestthree = 0
        try:
            kstandthree = g3.get_group(2).count() * 5 / 60  # get activity belog to 0,1,2,3
        except:
            kstandthree = 0
        try:
            kruningtthree = g3.get_group(0).count() * 5 / 60  # get activity belog to 0,1,2,3
        except:
            kruningtthree = 0
        try:
            kwalkingthree = g3.get_group(1).count() * 5 / 60  # get activity belog to 0,1,2,3
        except:
            kwalkingthree = 0

        ################### day 4 count action ###################
        try:
            krest4 = g4.get_group(3).count() * 5 / 60
        except:
            krest4 = 0
        try:
            kstand4 = g4.get_group(2).count() * 5 / 60
        except:
            kstand4 = 0
        try:
            kruning4 = g4.get_group(0).count() * 5 / 60
        except:
            kruning4 = 0
        try:
            kwalking4 = g4.get_group(1).count() * 5 / 60
        except:
            kwalking4 = 0

        ################### day 5 count action ###################
        try:
            krest5 = g5.get_group(3).count() * 5 / 60
        except:
            krest5 = 0
        try:
            kstand5 = g5.get_group(2).count() * 5 / 60
        except:
            kstand5 = 0
        try:
            kruning5 = g5.get_group(0).count() * 5 / 60
        except:
            kruning5 = 0
        try:
            kwalking5 = g5.get_group(1).count() * 5 / 60
        except:
            kwalking5 = 0

        ################### day 6 count action ###################
        try:
            krest6 = g6.get_group(3).count() * 5 / 60
        except:
            krest6 = 0
        try:
            kstand6 = g6.get_group(2).count() * 5 / 60
        except:
            kstand6 = 0
        try:
            kruning6 = g6.get_group(0).count() * 5 / 60
        except:
            kruning6 = 0
        try:
            kwalking6 = g6.get_group(1).count() * 5 / 60
        except:
            kwalking6 = 0

        ################### day 7 count action ###################
        try:
            krest7 = g7.get_group(3).count() * 5 / 60
        except:
            krest7 = 0
        try:
            kstand7 = g7.get_group(2).count() * 5 / 60
        except:
            kstand7 = 0
        try:
            kruning7 = g7.get_group(0).count() * 5 / 60
        except:
            kruning7 = 0
        try:
            kwalking7 = g7.get_group(1).count() * 5 / 60
        except:
            kwalking7 = 0

        ################### day 8 count action ###################
        try:
            krest8 = g8.get_group(3).count() * 5 / 60
        except:
            krest8 = 0
        try:
            kstand8 = g8.get_group(2).count() * 5 / 60
        except:
            kstand8 = 0
        try:
            kruning8 = g8.get_group(0).count() * 5 / 60
        except:
            kruning8 = 0
        try:
            kwalking8 = g8.get_group(1).count() * 5 / 60  # Atention DATA POINT CHANGED HERE FOR HACK DATA MANIPULATE
        except:
            kwalking8 = 0

        ################### day 9 count action ###################
        try:
            krest9 = g9.get_group(3).count() * 5 / 60
        except:
            krest9 = 0
        try:
            kstand9 = g9.get_group(2).count() * 5 / 60
        except:
            kstand9 = 0
        try:
            kruning9 = g9.get_group(0).count() * 5 / 60
        except:
            kruning9 = 0
        try:
            kwalking9 = g9.get_group(1).count() * 5 / 60
        except:
            kwalking9 = 0

        ################### day 10 count action ###################
        try:
            krest10 = g10.get_group(3).count() * 5 / 60
        except:
            krest10 = 0
        try:
            kstand10 = g10.get_group(2).count() * 5 / 60
        except:
            kstand10 = 0
        try:
            kruning10 = g10.get_group(0).count() * 5 / 60
        except:
            kruning10 = 0
        try:
            kwalking10 = g10.get_group(1).count() * 5 / 60
        except:
            kwalking10 = 0

        restlist = [kresttwo, krestthree, krest4, krest5, krest6, krest7, krest8, krest9, krest10]
        standlist = [kstandtwo, kstandthree, kstand4, kstand5, kstand6, kstand7, kstand8, kstand9, kstand10]
        runninglist = [kruningtwo, kruningtthree, kruning4, kruning5, kruning6, kruning7, kruning8, kruning9, kruning10]
        walkinglist = [kwalkingtwo, kwalkingthree, kwalking4, kwalking5, kwalking6, kwalking7, kwalking8, kwalking9,
                       kwalking10]

        # chum = (krest + kresttwo + krestthree)/3
        totalrestlist = np.mean(restlist[0: self.choselist])
        totalstandinglist = np.mean(standlist[0: self.choselist])
        totalrunninglist = np.mean(runninglist[0: self.choselist])
        totalwalkinglist = np.mean(walkinglist[0: self.choselist])

        # print(kstand)
        # print(kstandtwo)
        # print(kstandthree)
        persentrest = (pd.to_numeric(((krest / (totalrestlist)) * 100)).loc['activity'])
        persentstand = (pd.to_numeric(((kstand / (totalstandinglist)) * 100)).loc['activity'])
        persentrunning = (pd.to_numeric(((kruning / (totalrunninglist)) * 100)).loc['activity'])
        persentwalking = (pd.to_numeric(((kwalking / (totalwalkinglist)) * 100)).loc['activity'])

        coll_persent_of_kdays_actions = (persentrest, persentstand, persentrunning, persentwalking)
        summarizecon = sum(coll_persent_of_kdays_actions)
        summarize = sum(coll_persent_of_kdays_actions) / 4
        # maxvalue = max(persentrest, persentstand, persentrunning, persentwalking)
        Difference_Bihavior_percent = ((summarize / summarizecon) * 100)
        healthgood = 0
        healthwarning = 0
        healthbad = 0
        if summarize <= 10:
            print("Health Good")
            healthgood = 300
        if (summarize > 10) and (summarize < 20):
            print("Health Warning")
            healthwarning = 300
        if summarize > 20:
            print("Health Bad")
            healthbad = 300

        hlgood(healthgood)
        hlwarming(healthwarning)
        hlbad(healthbad)


while True:
    t1.setDaemon(True)
    t1.start()
    t1.join()
    sleep(6)







