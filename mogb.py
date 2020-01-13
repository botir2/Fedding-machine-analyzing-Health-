# Import libraries
import pandas as pd
import pymysql
from pip._vendor.distlib.compat import raw_input
from pymongo import MongoClient
import pymongo
from decimal import Decimal
import numpy as np
from datetime import datetime, timedelta
from sshtunnel import SSHTunnelForwarder
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
        MONGO_HOST = "222.116.135.117"
        MONGO_DB = "petness"
        MONGO_USER = "pi"
        MONGO_PASS = "niceduri"

        server = SSHTunnelForwarder(
            MONGO_HOST,
            ssh_username=MONGO_USER,
            ssh_password=MONGO_PASS,
            remote_bind_address=('127.0.0.1', 27017)
        )
        server.start()
        # Connection to the MongoDB Server
        mongoClient = MongoClient('127.0.0.1', server.local_bind_port)  # server.local_bind_port is assigned local port
        # Connection to the database
        db = mongoClient[MONGO_DB]
        # Collection
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
        detailsrowtoday = collection.find({'date': {"$regex": today}})
        dftoday = pd.DataFrame(list(detailsrowtoday))
        gtaday = dftoday.groupby("activity")
        self.resttoday = gtaday.get_group(0).count() * 5  # get activity belog to 0,1,2,3
        self.standtoday = gtaday.get_group(1).count() * 5  # get activity belog to 0,1,2,3
        self.runningtoday = gtaday.get_group(2).count() * 5
        self.walkingtoday = gtaday.get_group(3).count() * 5


    ################################# K days functions###################################################
    def twodaysrest(self):
        detailsrow1 = self.collection.find({'date': {"$regex": self.one_day_ago}})
        detailsrow2 = self.collection.find({'date': {"$regex": self.two_days_ago}})

        df = pd.DataFrame(list(detailsrow1))  # one day ago
        df2 = pd.DataFrame(list(detailsrow2))

        g = df.groupby("activity")  # one day ago
        g2 = df2.groupby("activity")

        krest = g.get_group(0).count() * 5  # get activity belog to 0,1,2,3
        kstand = g.get_group(1).count() * 5  # get activity belog to 0,1,2,3
        kruning = g.get_group(2).count() * 5  # get activity belog to 0,1,2,3
        kwalking = g.get_group(3).count() * 5  # get activity belog to 0,1,2,3

        kresttwo = g2.get_group(0).count() * 5  # get activity belog to 0,1,2,3
        kstandtwo = g2.get_group(1).count() * 5  # get activity belog to 0,1,2,3
        kruningtwo = g2.get_group(2).count() * 5  # get activity belog to 0,1,2,3
        kwalkingtwo = g2.get_group(3).count() * 5  # get activity belog to 0,1,2,3



        totalrest = (pd.to_numeric((100 - ((self.resttoday / ((krest + kresttwo) / 2)) * 100)).loc['activity']))
        totalstand = (pd.to_numeric((100 - ((self.resttoday / ((kstand + kstandtwo) / 2)) * 100)).loc['activity']))
        totalrunning = (pd.to_numeric((100 - ((self.resttoday / ((kruning + kruningtwo) / 2)) * 100)).loc['activity']))
        totalwalking = (pd.to_numeric((100 - ((self.resttoday / ((kwalking + kwalkingtwo) / 2)) * 100)).loc['activity']))

        #calculation = pd.to_numeric(totalrest.loc['activity'])
        print(kstand)
        print(kstandtwo)


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

        krest = g.get_group(0).count() * 5  # get activity belog to 0,1,2,3
        kstand = g.get_group(1).count() * 5  # get activity belog to 0,1,2,3
        kruning = g.get_group(2).count() * 5  # get activity belog to 0,1,2,3
        kwalking = g.get_group(3).count() * 5  # get activity belog to 0,1,2,3

        kresttwo = g2.get_group(0).count() * 5  # get activity belog to 0,1,2,3
        kstandtwo = g2.get_group(1).count() * 5  # get activity belog to 0,1,2,3
        kruningtwo = g2.get_group(2).count() * 5  # get activity belog to 0,1,2,3
        kwalkingtwo = g2.get_group(3).count() * 5  # get activity belog to 0,1,2,3

        krestthree = g3.get_group(0).count() * 5  # get activity belog to 0,1,2,3
        kstandthree = g3.get_group(1).count() * 5  # get activity belog to 0,1,2,3
        kruningtthree = g3.get_group(2).count() * 5  # get activity belog to 0,1,2,3
        kwalkingthree = g3.get_group(3).count() * 5  # get activity belog to 0,1,2,3

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


        g = df.groupby("activity")  # one day ago
        g2 = df2.groupby("activity")
        g3 = df3.groupby("activity")
        g4 = df4.groupby("activity")  # one day ago
        g5 = df5.groupby("activity")
        g6 = df6.groupby("activity")
        g7 = df7.groupby("activity")  # one day ago
        g8 = df8.groupby("activity")
        g9 = df9.groupby("activity")
        g10 = df10.groupby("activity")
        print(g9)

        try:
            krest = g.get_group(0).count() * 5  # get activity belog to 0,1,2,3
            kstand = g.get_group(1).count() * 5  # get activity belog to 0,1,2,3
            kruning = g.get_group(2).count() * 5  # get activity belog to 0,1,2,3
            kwalking = g.get_group(3).count() * 5  # get activity belog to 0,1,2,3

            kresttwo = g2.get_group(0).count() * 5  # get activity belog to 0,1,2,3
            kstandtwo = g2.get_group(1).count() * 5  # get activity belog to 0,1,2,3
            kruningtwo = g2.get_group(2).count() * 5  # get activity belog to 0,1,2,3
            kwalkingtwo = g2.get_group(3).count() * 5  # get activity belog to 0,1,2,3

            krestthree = g3.get_group(0).count() * 5  # get activity belog to 0,1,2,3
            kstandthree = g3.get_group(1).count() * 5  # get activity belog to 0,1,2,3
            kruningtthree = g3.get_group(2).count() * 5  # get activity belog to 0,1,2,3
            kwalkingthree = g3.get_group(3).count() * 5  # get activity belog to 0,1,2,3

            krest4 = g4.get_group(0).count() * 5
            kstand4 = g4.get_group(1).count() * 5
            kruning4 = g4.get_group(2).count() * 5
            kwalking4 = g4.get_group(3).count() * 5

            krest5 = g5.get_group(0).count() * 5
            kstand5 = g5.get_group(1).count() * 5
            kruning5 = g5.get_group(2).count() * 5
            kwalking5 = g5.get_group(3).count() * 5

            krest6 = g6.get_group(0).count() * 5
            kstand6 = g6.get_group(1).count() * 5
            kruning6 = g6.get_group(2).count() * 5
            kwalking6 = g6.get_group(3).count() * 5

            krest7 = g7.get_group(0).count() * 5
            kstand7 = g7.get_group(1).count() * 5
            kruning7 = g7.get_group(2).count() * 5
            kwalking7 = g7.get_group(3).count() * 5

            krest8 = g8.get_group(0).count() * 5
            kstand8 = g8.get_group(1).count() * 5
            kruning8 = g8.get_group(2).count() * 5
            kwalking8 = g8.get_group(3).count() * 5 # Atention DATA POINT CHANGED HERE FOR HACK DATA MANIPULATE

            krest9 = g9.get_group(0).count() * 5
            kstand9 = g9.get_group(1).count() * 5
            kruning9 = g9.get_group(2).count() * 5
            kwalking9 = g9.get_group(3).count() * 5

            krest10 = g10.get_group(0).count() * 5
            kstand10 = g10.get_group(1).count() * 5
            kruning10 = g10.get_group(2).count() * 5
            kwalking10 = g10.get_group(3).count() * 5

        except:

            kwalking10 = 0



        restlist = [krest, kresttwo, krestthree, krest4, krest5, krest6, krest7, krest8, krest9, krest10]
        standlist = [kstand, kstandtwo, kstandthree, kstand4, kstand5, kstand6, kstand7, kstand8, kstand9, kstand10]
        runninglist = [kruning, kruningtwo, kruningtthree, kruning4, kruning5, kruning6, kruning7, kruning8, kruning9, kruning10]
        walkinglist = [kwalking, kwalkingtwo, kwalkingthree, kwalking4, kwalking5, kwalking6, kwalking7, kwalking8,kwalking9, kwalking10]

        totalrestlist = np.mean(restlist[0: choselist])
        totalstandinglist = np.mean(standlist[0: choselist])
        totalrunninglist = np.mean(runninglist[0: choselist])
        totalwalkinglist = np.mean(walkinglist[0: choselist])

        #print(kstand)
        #print(kstandtwo)
        #print(kstandthree)
        persentrest = (pd.to_numeric(((self.resttoday / (totalrestlist)) * 100)).loc['activity'])
        persentstand = (pd.to_numeric(((self.resttoday / (totalstandinglist)) * 100)).loc['activity'])
        persentrunning = (pd.to_numeric(((self.resttoday / (totalrunninglist)) * 100)).loc['activity'])
        persentwalking = (pd.to_numeric(((self.resttoday / (totalwalkinglist)) * 100)).loc['activity'])

        totalrest = (pd.to_numeric((100 - ((self.resttoday / (totalrestlist)) * 100)).loc['activity']))
        totalstand = (pd.to_numeric((100 - ((self.standtoday / (totalstandinglist)) * 100)).loc['activity']))
        totalrunning = (pd.to_numeric((100 - ((self.runningtoday / (totalrunninglist)) * 100)).loc['activity']))
        totalwalking = (pd.to_numeric((100 - ((self.walkingtoday / (totalwalkinglist)) * 100)).loc['activity']))

        # calculation = pd.to_numeric(totalrest.loc['activity'])
        print(persentrest)
        print(persentstand)
        print(persentrunning)
        print(persentwalking)

        N = 4

        yesterday = (2, 154, 14, 3)
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
    analyze.main(2)


    #analyze.twodaysrest()
    # chumchuq = 100-((analyze.main() /analyze.twodays( ))*100)
    # print(chumchuq)



