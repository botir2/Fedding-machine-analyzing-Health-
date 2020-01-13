#!/usr/bin/python
# encoding=utf8

import time
import pexpect
import subprocess
import sys
import bluetooth
import connection_class
import json
from pymongo import MongoClient
import datetime
import pymysql
import random
import threading
from datetime import datetime, timedelta

target_name = "HC-05"  # Device name
port = 1  # RFCOMM port
target_address = None
End = '\n'  # something useable as an end marker
DATABASE_URL = "mongodb://localhost:27017"


#
################################################################################
#
#   Insert DB server
#
def InsertDB(device_uuid, resting, staying, walking, running, health_good, health_warming, health_bad, date):
    conn = pymysql.connect(host='211.38.86.93',
                           user='root',
                           password='niceduri',
                           db='Pet-it',
                           charset='utf8')
    try:
        with conn.cursor() as cursor:
            #           sql = 'INSERT INTO behavior_log(uuid, resting, staying, walking, running, health_status, date TOKEN) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            #           cursor.execute(sql, (behavoir of pit action token_string))
            sql = 'INSERT INTO bahavoir (uuid, resting, staying, walking, running, health_good, health_warning, health_bad, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (
            device_uuid, resting, staying, walking, running, health_good, health_warming, health_bad, date))
            conn.commit()
            print(cursor.lastrowid)
    finally:
        conn.close()
    return cursor.lastrowid



#
################################################################################
#
#   Main Routine
#

if __name__ == "__main__":
    target_address = "98:D3:31:40:4A:07"
    #timecha = datetime.now().strftime('%Y-%m-26 %H:%M:%S')
    #seconds = datetime.now() +timedelta(seconds=5).strftime("%H:%M:%S")
    #seconds = (datetime.datetime.now() + datetime.timedelta(seconds=5)).strftime("%H:%M:%S")
    while True:
        try:
            minutes = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%H:%M:%S")
            # ran = random.randint(0, 300)
            # for rs, st, wl, rn in range((ran),4):
            # print(rs,st,wl,rn)
            # rs, st, wl, rn = random.sample(range(0, 300), 4)
            rs = random.randint(0, 300)
            st = random.randint(0, 300)
            wl = random.randint(0, 300)
            rn = random.randint(0, 300)
            joint = rs + st + wl + rn
            if joint == 300:
                print("InsertTo db: ", rs, ": ", st, ": ", wl, ": ", rn, "time: ", seconds)
            # InsertDB(target_address, rs, st, wl, rn, 300, 0, 0, timecha)
            # print("InsertTo db: ",rs,": ", st,": ",wl,": ",rn,"time: ",timecha)
            # time.sleep(1)
        except:
            print("Error")






