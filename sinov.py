from pymongo import MongoClient
import pymongo
from decimal import Decimal
import numpy as np
from datetime import datetime, timedelta

RestM =[]
RunM = []
WalkM =[]
StandM=[]

fRun = open('running.txt', 'r+')
Runnes = fRun.readlines()
for val in Runnes[-1].split():
    RunM.append(int(val))
    Run=int(RunM[-1])
fRest = open('resting.txt', 'r+')
Restnes = fRest.readlines()
for val in Restnes[-1].split():
    RestM.append(int(val))
    Rest=int(RestM[-1])
fWalk = open('walking.txt', 'r+')
Walknes = fWalk.readlines()
for val in Walknes[-1].split():
    WalkM.append(int(val))
    Walk=int(WalkM[-1]) 
fStand = open('standing.txt', 'r+')
Standnes = fStand.readlines()
for val in Standnes[-1].split():
    StandM.append(int(val))
    Stand=int(StandM[-1]) 

#rr=RestM[-2]
M_rest=np.mean(RestM)
M_run=np.mean(RunM)
M_walk=np.mean(WalkM)
M_stand=np.mean(StandM)
print(Stand)
diffRe=Rest-M_rest
diffRu=Run-M_run
diffWa=Walk-M_walk
diffSt=Stand-M_stand
print("Difference Resting  ", round(diffRe,2))
print("Difference Running  ", round(diffRu,2))
print("Difference Walking  ", round(diffWa,2))
print("Difference Standing ", round(diffSt,2))
perRe=(Rest*100)/M_rest
perRu=(Run*100)/M_run
perWa=(Walk*100)/M_walk
perSt=(Stand*100)/M_stand
print("Percent Resting  ", round(perRe,2))
print("Percent Running  ", round(perRu,2))
print("Percent Walking  ", round(perWa,2))
print("Percent Standing ", round(perSt,2))
Sum=(perRe+perRu+perWa+perSt)/4
print(abs(100-Sum))


