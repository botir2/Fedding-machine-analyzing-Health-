# Import libraries
import pandas as pd
import pymysql
from pymongo import MongoClient
import pymongo
from decimal import Decimal
import numpy as np
from datetime import datetime, timedelta
from sshtunnel import SSHTunnelForwarder

MONGO_HOST = "222.116.135.106"
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
client = MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
db = client[MONGO_DB]
print(db.collection_names())
server.stop()


