# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 18:35:54 2021

@author: Bugra
"""

import psycopg2
import matplotlib.pyplot as plt
import matplotlib
from datetime import timedelta
from datetime import datetime

#Step 2: Connect to the database
try:
    f = open("database.txt", "r")
    database=f.readline().rstrip("\n")
    user=f.readline().rstrip("\n")
    password=f.readline().rstrip("\n")
    host=f.readline().rstrip("\n")
    port=f.readline().rstrip("\n")
    conn = psycopg2.connect(database=database,
                        user=user,
                        password=password,
                        host=host,
                        port=port)

    print("Successfully Connected")
except:
    print("Connection failed")
    

cur = conn.cursor()

query2 =  """select DISTINCT mmsi,lat,lon,time_info
from ships_opt_10_12
where ship_type='Passenger'
order by mmsi,time_info
"""

cur.execute(query2)

passengers=cur.fetchall()
passenger_list=[]
before_pos=[0,0]
before_vessel=""
before_time=""
distance_threshold=20
time_threshold =timedelta(minutes=10)
#unwanted_vessels=[]
for passanger in passengers:
    mmsi=passanger[0]
    latitude=passanger[1]
    longitude=passanger[2]
    timee=str(passanger[3])
    print(timee)
    timee2 = timee.split(" ")
    datee=timee2[0].split("-")
    clock=timee2[1].split(":")

    b = datetime(int(datee[0]), int(datee[1]), int(datee[2]),int(clock[0]) , int(clock[1]), int(clock[2]), 00)

    if(before_vessel==""):
        before_pos=[latitude,longitude]
        before_vessel=mmsi
        before_time=b
        passenger_list.append(mmsi)
    else:
        if(mmsi==before_vessel):
            #do something
            dist_query= " SELECT ST_Distance( "\
                		" 'SRID=4326;POINT({} {})'::geometry, "\
            		    " 'SRID=4326;POINT({} {})'::geometry "\
            	        " ) ".format(before_pos[0],before_pos[1],latitude,longitude)
            
            cur.execute(dist_query)
    
            distance = cur.fetchall()
            
            for dist in distance:
                if(dist[0]>distance_threshold):
                    before_pos=[latitude,longitude]
                    before_vessel=mmsi
                    before_time=b
                    #unwanted_vessels.append(mmsi)
                    if(len(passenger_list)>0):
                        if(passenger_list[-1]==mmsi):
                            passenger_list.pop()
                elif(b-before_time>time_threshold):
                    before_pos=[latitude,longitude]
                    before_vessel=mmsi
                    before_time=b
                    #unwanted_vessels.append(mmsi)
                    if(len(passenger_list)>0):
                        if(passenger_list[-1]==mmsi):
                            passenger_list.pop()
                else:
                    before_pos=[latitude,longitude]
                    before_vessel=mmsi
                    before_time=b
                    #if(passenger_list[-1]!=mmsi):
                    #    if(mmsi in unwanted_vessels==False):
                    #        passenger_list.append(mmsi)
        else:
            before_pos=[latitude,longitude]
            before_vessel=mmsi
            before_time=b
            passenger_list.append(mmsi)
    #passenger_list.append(passanger[0])
    

# GPS hatası olan gemiler elemine edildi


# Simple solution - Loop------------

file = open("trajectory_ships_20min_v2.txt", "w")
for ship in passenger_list:
    sog_value=0.5
    query = " select mmsi,time_info,sog " \
            " from ships_1012_geom s"\
            " FULL JOIN zones z1 ON ST_Dwithin(z1.geom, s.geom,0.003) "\
            " where mmsi={} and sog<{} "\
            " order by time_info desc ".format(ship,sog_value)
    
    cur.execute(query)
    
    rows = cur.fetchall()

    before_time=""
    i=0
    threshold_time=timedelta(hours = 0, minutes = 20, seconds = 0)
    for row in (rows):
        #indx = rows.index(row)
        if(before_time==""):
            before_time=row[1]
        else:
            result=before_time-row[1]
            if(result>threshold_time):
                i=i+1
                file.write(str(row[0])+" ") #mmsi
                file.write(str(i)+" ") #id 
                file.write(str(row[1])+" ") #time_start
                file.write(str(row[1]+result)+" ") #time_finish
                file.write(str(result)+" ") #duration
                file.write("\n") 
            before_time=row[1]
                
    
file.close()
cur.close()
conn.close()
