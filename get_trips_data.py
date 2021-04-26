# seçilen geminin yolculuk verilerini csv dosyasına yazdırır.

from trajectory import *
from datetime import datetime
from datetime import timedelta
import math
import csv

# database connection
f = open("database.txt", "r")
database=f.readline().rstrip("\n")
user=f.readline().rstrip("\n")
password=f.readline().rstrip("\n")
host=f.readline().rstrip("\n")
port=f.readline().rstrip("\n")
p = postgres(database, user,password,host,port)

#INPUTS
stage=4 # yolculuğun kaçancı parçası alınacak
default_mmsi=219005068
table_name="ships"
time_range=timedelta(minutes=10)

# ANALYSE
f2 = open("trajectory_ships_20min_219005068_local.txt", "r")

with open('219005068_10min_'+str(stage)+'.csv', mode='w') as csv_file:
    points_fieldnames = ['time', 'lat', 'lon']
    writer = csv.DictWriter(csv_file, fieldnames=points_fieldnames)
    writer.writeheader()
    
    for x in f2:
        line=x.split()
        mmsi=line[0]

        if mmsi==str(default_mmsi):
            datee=line[2]
            datee=datee.split("-")
            start_time=line[3].split(":")
            start_time2=line[2]+" "+line[3]

            finish_time=line[5].split(":")
            finish_time2=line[4]+" "+line[5]
            finish_epoch=datetime(int(datee[0]),int(datee[1]),int(datee[2]),int(finish_time[0]),int(finish_time[1]),int(finish_time[2]))
            epoch1=datetime(int(datee[0]),int(datee[1]),int(datee[2]),int(start_time[0]),int(start_time[1]),int(start_time[2]))+(time_range*(stage-1))
            epoch2=epoch1+time_range

            print(epoch1)
            print(epoch2)
            # get points 
            points_info=p.getVesselSpecificTimewithTimeInfo(table_name,mmsi,epoch1,epoch2)
            for poi in points_info:
                    writer.writerow({'time': poi[2],'lat':poi[1],'lon':poi[0] })


