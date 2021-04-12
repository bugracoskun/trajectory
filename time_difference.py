# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 18:35:54 2021

@author: Bugra
"""
from trajectory import *
import psycopg2
from datetime import timedelta
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#Step 2: Connect to the database
f = open("database.txt", "r")
database=f.readline().rstrip("\n")
user=f.readline().rstrip("\n")
password=f.readline().rstrip("\n")
host=f.readline().rstrip("\n")
port=f.readline().rstrip("\n")
p = postgres(database, user,password,host,port)
    

cur = p.conn.cursor()

table_name='ships_1012_geom'
mmsi='219005068 '
start_time='2020-12-10 00:00:00'
end_time='2020-12-10 01:00:00'

times=p.getVesselTimeDiff(table_name,mmsi,start_time,end_time)

diff=[]

before_time=""
for time in times:
    if(before_time==""):
        before_time=time[0]
    else:
        td=time[0]-before_time
        if(td.total_seconds()!=0):
            diff.append(td.total_seconds())
        before_time=time[0]

# Data for plotting
t = diff
s = range(0, len(diff))

fig, ax = plt.subplots()
ax.plot(s, t)

ax.set(xlabel='observations', ylabel='seconds',
       title='Time Difference')
ax.grid()

plt.show()

cur.close()
