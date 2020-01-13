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
        last_eleven = datetime.now() - timedelta(days=11)
        self.one_day_ago = last_day_one.strftime("%Y-%m-%d %H:%M")
        self.two_days_ago = last_day_two.strftime("%Y-%m-%d %H:%M")
        self.three_days_ago = last_day_three.strftime("%Y-%m-%d %H:%M")
        self.four_dyas_ago = last_day_four.strftime("%Y-%m-%d %H:%M")
        self.fife_days_ago = last_day_five.strftime("%Y-%m-%d %H:%M")
        self.six_days_ago = last_day_six.strftime("%Y-%m-%d %H:%M")
        self.seven_days_ago = last_day_seven.strftime("%Y-%m-%d %H:%M")
        self.eight_days_ago = last_day_eight.strftime("%Y-%m-%d %H:%M")
        self.nine_days_ago = last_day_nine.strftime("%Y-%m-%d %H:%M")
        self.ten_days_ago = last_day_ten.strftime("%Y-%m-%d %H:%M")
        self.eleven_days_ago = last_eleven.strftime("%Y-%m-%d %H:%M")

        ################################# Mong db result ##################################
        # Connection to the MongoDB Server
        mongoClient = MongoClient("mongodb://localhost:27017")
        # Connection to the database
        db = mongoClient["petness"]
        # Collection
        collection = db["dog"]
        self.collection = collection
        today = datetime.now().strftime('%Y-%m-%d')
        # detailsrow = collection.find({'date': {"$regex": self.thre_days_ago}})
        detailsrow = collection.find({'date': {"$regex": self.three_days_ago}})
        detailsrow2 = collection.find({'date': {"$regex": self.one_day_ago}})
        # detail = collection.find()
        # df = pd.DataFrame(list(detailsrow2))
        # df2 = pd.DataFrame(list(detailsrow))
        # df3 = pd.DataFrame(list(detailsrowtoday))
        # df[df['activity'] == 0].count()
        # df.groupby('activity').activity.count()
        # df[df['activity'] == 1].count()
        # df.asfreq(freq='5S')
        # g = df.groupby("activity")
        # g2 = df2.groupby("activity")
        # g3 = df3.groupby("activity")
        # df.groupby("activity"(freq='D')).ffill()
        # tday = g.get_group(0).count() * 5 #get activity belog to 0,1,2,3
        # two = g2.get_group(0).count() * 5
        # four = g3.get_group(0).count() * 5
        # two = g.get_group(2).count()
        # three = ((tday + two) / 2) / four * 100 - 100
        # self.three = three
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        # detailsrow = collection.find({'date': {"$regex": self.thre_days_ago}})
        #detailsrow = collection.find({'date': {"$regex": self.three_days_ago}})
        #detailsrow2 = collection.find({'date': {"$regex": self.one_day_ago}})
        # detail = collection.find()
        # df = pd.DataFrame(list(detailsrow2))
        # df2 = pd.DataFrame(list(detailsrow))
        # df3 = pd.DataFrame(list(detailsrowtoday))
        # df[df['activity'] == 0].count()
        # df.groupby('activity').activity.count()
        # df[df['activity'] == 1].count()
        # df.asfreq(freq='5S')
        # g = df.groupby("activity")
        # g2 = df2.groupby("activity")
        # g3 = df3.groupby("activity")
        # df.groupby("activity"(freq='D')).ffill()
        # tday = g.get_group(0).count() * 5 #get activity belog to 0,1,2,3
        # two = g2.get_group(0).count() * 5
        # four = g3.get_group(0).count() * 5
        # two = g.get_group(2).count()
        # three = ((tday + two) / 2) / four * 100 - 100
        # self.three = three
        detailsrowtoday = collection.find({'date': {'$gte': self.one_day_ago, '$lte': today}}) #add 24 hours date obtainong
        dftoday = pd.DataFrame(list(detailsrowtoday))
        gtaday = dftoday.groupby("activity")
        try:
            self.resttoday = gtaday.get_group(3).count() * 5 / 60# get activity belog to 0,1,2,3
        except:
            self.resttoday = 0
        try:
            self.standtoday = gtaday.get_group(2).count() * 5 / 60  # get activity belog to 0,1,2,3
        except:
            self.standtoday = 0
        try:
            self.runningtoday = gtaday.get_group(0).count() * 5 / 60
        except:
            self.runningtoday = 0
        try:
            self.walkingtoday = gtaday.get_group(1).count() * 5 / 60
        except:
            self.walkingtoday = 0



################################# K days functions###################################################
    def twodaysrest(self):
        detailsrow1 = self.collection.find({'date': {'$gte': self.two_days_ago, '$lte': self.one_day_ago}})
        detailsrow2 = self.collection.find({'date': {'$gte': self.three_days_ago, '$lte': self.two_days_ago}})

        df = pd.DataFrame(list(detailsrow1))  # one day ago
        df2 = pd.DataFrame(list(detailsrow2))

        g = df.groupby("activity")  # one day ago
        g2 = df2.groupby("activity")

        krest = g.get_group(3).count() * 5  # get activity belog to 0,1,2,3
        kstand = g.get_group(2).count() * 5  # get activity belog to 0,1,2,3
        kruning = g.get_group(0).count() * 5  # get activity belog to 0,1,2,3
        kwalking = g.get_group(1).count() * 5  # get activity belog to 0,1,2,3

        kresttwo = g2.get_group(3).count() * 5  # get activity belog to 0,1,2,3
        kstandtwo = g2.get_group(2).count() * 5  # get activity belog to 0,1,2,3
        kruningtwo = g2.get_group(0).count() * 5  # get activity belog to 0,1,2,3
        kwalkingtwo = g2.get_group(1).count() * 5  # get activity belog to 0,1,2,3



        totalrest = (pd.to_numeric(((self.resttoday / ((krest + kresttwo) / 2)) * 100).loc['activity']))
        totalstand = (pd.to_numeric(((self.standtoday / ((kstand + kstandtwo) / 2)) * 100).loc['activity']))
        totalrunning = (pd.to_numeric(((self.runningtoday / ((kruning + kruningtwo) / 2)) * 100).loc['activity']))
        totalwalking = (pd.to_numeric(((self.walkingtoday / ((kwalking + kwalkingtwo) / 2)) * 100).loc['activity']))

        #calculation = pd.to_numeric(totalrest.loc['activity'])
        print(kstand)
        print(kstandtwo)


        N = 4

        yesterday = (totalrest, totalstand, totalrunning, totalwalking)
        today = (1, 1, 1, 1)
        menStd = (3, 3, 3, 3)
        womenStd = (3, 3, 3, 3)
        ind = np.arange(N)  # the x locations for the groups
        width = 0.65  # the width of the bars: can also be len(x) sequence

        p1 = plt.bar(ind, today, width, yerr=menStd)
        p2 = plt.bar(ind, yesterday, width,
                     bottom=today, yerr=womenStd)

        plt.ylabel('Scores')
        plt.title('Scores by group and gender')
        plt.xticks(ind, ('Resting', 'Standing', 'Running', 'Walking'))
        plt.yticks(np.arange(0, 200, 20))
        plt.legend((p1[0], p2[0]), ('Today', '2K_days'))

        plt.show()


        # plt.plot([totalrest, totalstand, totalrunning, totalwalking])
        #plt.plot([1,-2,3,4,-5])
        #plt.ylabel('action %')
        #plt.show()
        df2.plot.bar();

    def threedaysresult(self):

        detailsrow1 = self.collection.find({'date': {"$regex": self.one_day_ago}})
        detailsrow2 = self.collection.find({'date': {"$regex": self.two_days_ago}})
        detailsrow3 = self.collection.find({'date': {"$regex": self. three_days_ago}})

        df = pd.DataFrame(list(detailsrow1))  # one day ago
        df2 = pd.DataFrame(list(detailsrow2))
        df3 = pd.DataFrame(list(detailsrow3))

        g = df.groupby("activity")  # one day ago
        g2 = df2.groupby("activity")
        g3 = df3.groupby("activity")

        krest = g.get_group(3).count() * 5  # get activity belog to 0,1,2,3
        kstand = g.get_group(2).count() * 5  # get activity belog to 0,1,2,3
        kruning = g.get_group(0).count() * 5  # get activity belog to 0,1,2,3
        kwalking = g.get_group(1).count() * 5  # get activity belog to 0,1,2,3

        kresttwo = g2.get_group(3).count() * 5  # get activity belog to 0,1,2,3
        kstandtwo = g2.get_group(2).count() * 5  # get activity belog to 0,1,2,3
        kruningtwo = g2.get_group(0).count() * 5  # get activity belog to 0,1,2,3
        kwalkingtwo = g2.get_group(1).count() * 5  # get activity belog to 0,1,2,3

        krestthree = g3.get_group(3).count() * 5  # get activity belog to 0,1,2,3
        kstandthree = g3.get_group(2).count() * 5  # get activity belog to 0,1,2,3
        kruningtthree = g3.get_group(1).count() * 5  # get activity belog to 0,1,2,3
        kwalkingthree = g3.get_group(2).count() * 5  # get activity belog to 0,1,2,3

        totalrest = (pd.to_numeric((100 - ((self.resttoday / ((krest + kresttwo + krestthree) / 3)) * 100)).loc['activity']))
        totalstand = (pd.to_numeric((100 - ((self.resttoday / ((kstand + kstandtwo + kstandthree) / 3)) * 100)).loc['activity']))
        totalrunning = (pd.to_numeric((100 - ((self.resttoday / ((kruning + kruningtwo + kruningtthree) / 3)) * 100)).loc['activity']))
        totalwalking = (pd.to_numeric((100 - ((self.resttoday / ((kwalking + kwalkingtwo + kwalkingthree) / 3)) * 100)).loc['activity']))

        # calculation = pd.to_numeric(totalrest.loc['activity'])
        #print(krest)
        #print(kresttwo)
       #print(krestthree)

        N = 4

        yesterday = (totalrest, totalstand, totalrunning, totalwalking)
        today = (100, 100, 100, 100)
        menStd = (3, 3, 3, 3)
        womenStd = (3, 3, 3, 3)
        ind = np.arange(N)  # the x locations for the groups
        width = 0.65  # the width of the bars: can also be len(x) sequence

        p1 = plt.bar(ind, today, width, yerr=menStd)
        p2 = plt.bar(ind, yesterday, width,
                     bottom=today, yerr=womenStd)

        plt.ylabel('Scores')
        plt.title('Scores by group and gender')
        plt.xticks(ind, ('Resting', 'Standing', 'Running', 'Walking'))
        plt.yticks(np.arange(0, 200, 20))
        plt.legend((p1[0], p2[0]), ('Today', '3K_days'))

        plt.show()

        # plt.plot([totalrest, totalstand, totalrunning, totalwalking])
        # plt.plot([1,-2,3,4,-5])
        # plt.ylabel('action %')
        # plt.show()
        df2.plot.bar();



#######################################main function###################################################
    def main(self, choselist):
        detailsrow1 = self.collection.find( {'date': {'$gte': self.two_days_ago, '$lte': self.one_day_ago}})
        detailsrow2 = self.collection.find({'date': {'$gte': self.three_days_ago, '$lte': self.two_days_ago}})
        detailsrow3 = self.collection.find({'date': {'$gte': self.four_dyas_ago, '$lte': self.three_days_ago}})
        detailsrow4 = self.collection.find({'date': {'$gte': self.fife_days_ago, '$lte': self.four_dyas_ago}})
        detailsrow5 = self.collection.find({'date': {'$gte': self.six_days_ago, '$lte': self.fife_days_ago}})
        detailsrow6 = self.collection.find({'date': {'$gte': self.seven_days_ago, '$lte': self.six_days_ago}})
        detailsrow7 = self.collection.find({'date': {'$gte': self.eight_days_ago, '$lte': self.seven_days_ago}})
        detailsrow8 = self.collection.find({'date': {'$gte': self.nine_days_ago, '$lte': self.eight_days_ago}})
        detailsrow9 = self.collection.find({'date': {'$gte': self.ten_days_ago, '$lte': self.nine_days_ago}})
        detailsrow10 = self.collection.find({'date': {'$gte': self.eleven_days_ago, '$lte': self.ten_days_ago}})


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


        g = df.groupby("activity")  # one day ago
        g2 = df2.groupby("activity")
        g3 = df3.groupby("activity")
        g4 = df4.groupby("activity")  # one day ago
        g5 = df5.groupby("activity")
        g6 = df6.groupby("activity")
        try:
            g7 = df7.groupby("activity")  # one day ago
        except:
            g7 = 0
        try:
            g8 = df8.groupby("activity")
        except:
            g8 = 0
        g9 = df9.groupby("activity")
        g10 = df10.groupby("activity")
        #print(g9)

        ###################### day 1 count action ##############
        try:
            krest = g.get_group(3).count()* 5 / 60 # get activity belog to 0,1,2,3
        except:
            krest = 0
        try:
            kstand = g.get_group(2).count() * 5 / 60 # get activity belog to 0,1,2,3
        except:
            kstand = 0
        try:
            kruning = g.get_group(0).count() * 5 / 60 # get activity belog to 0,1,2,3
        except:
            kruning = 0
        try:
            kwalking = g.get_group(1).count() * 5 / 60 # get activity belog to 0,1,2,3
        except:
            kwalking = 0

        ###################### day 2 count action ################
        try:
            kresttwo = g2.get_group(3).count() * 5 / 60  # get activity belog to 0,1,2,3
        except:
            kresttwo = 0
        try:
            kstandtwo = g2.get_group(2).count() * 5 / 60# get activity belog to 0,1,2,3
        except:
            kstandtwo = 0
        try:
            kruningtwo = g2.get_group(0).count() * 5 / 60 # get activity belog to 0,1,2,3
        except:
            kruningtwo = 0
        try:
            kwalkingtwo = g2.get_group(1).count() * 5  / 60# get activity belog to 0,1,2,3
        except:
            kwalkingtwo = 0

        ################### day 3 count action ###################
        try:
            krestthree = g3.get_group(3).count() * 5 / 60# get activity belog to 0,1,2,3
        except:
            krestthree = 0
        try:
            kstandthree = g3.get_group(2).count() * 5 / 60# get activity belog to 0,1,2,3
        except:
            kstandthree = 0
        try:
            kruningtthree = g3.get_group(0).count() * 5 / 60 # get activity belog to 0,1,2,3
        except:
            kruningtthree = 0
        try:
            kwalkingthree = g3.get_group(1).count() * 5 / 60 # get activity belog to 0,1,2,3
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
            kwalking8 = g8.get_group(1).count() * 5  / 60# Atention DATA POINT CHANGED HERE FOR HACK DATA MANIPULATE
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



        restlist = [krest, kresttwo, krestthree, krest4, krest5, krest6, krest7, krest8, krest9, krest10]
        standlist = [kstand, kstandtwo, kstandthree, kstand4, kstand5, kstand6, kstand7, kstand8, kstand9, kstand10]
        runninglist = [kruning, kruningtwo, kruningtthree, kruning4, kruning5, kruning6, kruning7, kruning8, kruning9, kruning10]
        walkinglist = [kwalking, kwalkingtwo, kwalkingthree, kwalking4, kwalking5, kwalking6, kwalking7, kwalking8, kwalking9, kwalking10]

        chum = (krest + kresttwo + krestthree)/3
        totalrestlist = np.mean(restlist[0: choselist])
        totalstandinglist = np.mean(standlist[0: choselist])
        totalrunninglist = np.mean(runninglist[0: choselist])
        totalwalkinglist = np.mean(walkinglist[0: choselist])

        #print(kstand)
        #print(kstandtwo)
        #print(kstandthree)
        persentrest = (pd.to_numeric(((self.resttoday / (totalrestlist)) * 100)).loc['activity'])
        persentstand = (pd.to_numeric(((self.standtoday / (totalstandinglist)) * 100)).loc['activity'])
        persentrunning = (pd.to_numeric(((self.runningtoday / (totalrunninglist)) * 100)).loc['activity'])
        persentwalking = (pd.to_numeric(((self.walkingtoday / (totalwalkinglist)) * 100)).loc['activity'])

        coll_persent_of_kdays_actions = (persentrest, persentstand, persentrunning, persentwalking)
        summarize = sum(coll_persent_of_kdays_actions)
        maxvalue = max(persentrest, persentstand, persentrunning, persentwalking)
        Difference_Bihavior_percent = ((maxvalue / summarize) * 100)
        if Difference_Bihavior_percent < 50:
            print("Health Good")
        elif Difference_Bihavior_percent >= 50:
            print("Health Warning")
        elif Difference_Bihavior_percent <= 90:
            print("Health Bad")


        # calculation = pd.to_numeric(totalrest.loc['activity'])
        #print(self.resttoday)
        print(persentrest)
        print(persentstand)
        print(persentrunning)
        #print("________________")
        #print(self.standtoday)
        print(persentwalking)
        print(kstand8)
        print(kruning7)
        #print("________________")
        #print(chum)
        #print(totalrestlist)


        N = 4

        yesterday = (persentrest, persentstand, persentrunning, persentwalking)
        today = (1, 1, 1, 1)
        menStd = (3, 3, 3, 3)
        womenStd = (3, 3, 3, 3)
        ind = np.arange(N)  # the x locations for the groups
        width = 0.65  # the width of the bars: can also be len(x) sequence

        p1 = plt.bar(ind, today, width, yerr=menStd)
        p2 = plt.bar(ind, yesterday, width,
                     bottom=today, yerr=womenStd)

        plt.ylabel('Scores')
        plt.title('Scores by group days')
        plt.xticks(ind, ('Resting', 'Standing', 'Running', 'Walking'))
        plt.yticks(np.arange(0, 200, 20))
        plt.legend((p1[0], p2[0]), ('From 100%',  ''+str(choselist)+'K days'))

        plt.show()

        # plt.plot([totalrest, totalstand, totalrunning, totalwalking])
        # plt.plot([1,-2,3,4,-5])
        # plt.ylabel('action %')
        # plt.show()
        df2.plot.bar();



# analyze = datetimedays()


# Run = float(run)/3600
# time = pd.date_range(run, periods=2018, freq='5min')
# series = pd.Series(np.random.randint(100, size=2018), index=time)
# print(row)

if __name__ == '__main__':
    analyze = datetimedays()
    #analyze.twodaysrest()
    #analyze.threedaysresult()
    analyze.main(2)



    #analyze.twodaysrest()
    # chumchuq = 100-((analyze.main() /analyze.twodays( ))*100)
    # print(chumchuq)



