from trajectory import *
import requests
import psycopg2
from datetime import datetime
from datetime import timedelta
import math
from turf import point
from turf.center import center
import json
import csv


try:
    f = open("database.txt", "r")
    database=f.readline().rstrip("\n")
    user=f.readline().rstrip("\n")
    password=f.readline().rstrip("\n")
    host=f.readline().rstrip("\n")
    port=f.readline().rstrip("\n")
    appid=f.readline().rstrip("\n")
    p = postgres(database, user,password,host,port)

    # -------------------------------------------------------------
except:
    print("Connection failed")



bbox_area=[11.10499, 55.14280 ,11.26270, 55.23284]
cellSide=2
options = "{units: "+'kilometers'+"}"
grids=p.createGrids(bbox_area,cellSide,options)
table_name="ships_1012_geom"
space_time_cube_t="space_time_cube_10_12_2020_219005068"
default_mmsi=219005068
start_datee=datetime(2020,12,10, 00, 00, 00, 00)
add_time = timedelta(minutes=15)
border=5

# ------ Analyse -------------------

f2 = open("trajectory_ships_20min_v2.txt", "r")
data=[]
for x in f2:
    line=x.split()
    mmsi=line[0]
    if mmsi==str(default_mmsi):
        datee=line[2]
        start_time=line[3]
        start_time2=line[2]+" "+line[3]
        finish_time=line[5]
        finish_time2=line[4]+" "+line[5]
        datee=datee.split("-")
        start_time=start_time.split(":")
        finish_time=finish_time.split(":")
        epoch1=datetime(int(datee[0]),int(datee[1]),int(datee[2]),int(start_time[0]),int(start_time[1]),int(start_time[2])).timestamp()
        epoch2=datetime(int(datee[0]),int(datee[1]),int(datee[2]),int(finish_time[0]),int(finish_time[1]),int(finish_time[2])).timestamp()
        epoch=math.ceil((epoch1+epoch2)/2)
        
        date1=datetime(int(datee[0]),int(datee[1]),int(datee[2]),int(start_time[0]),int(start_time[1]),int(start_time[2]))
        date2=datetime(int(datee[0]),int(datee[1]),int(datee[2]),int(finish_time[0]),int(finish_time[1]),int(finish_time[2]))
        data.append(dict({"epoch":epoch,"start_time":start_time2,"start_time_obj":date1,"finish_time_obj":date2,"finish_time":finish_time2,"trip_time":line[6]}))

print(data[0])

all_date1=start_datee.strftime('%Y-%m-%d %H:%M:%S')
allPoints=p.getVesselAllLoc(table_name,default_mmsi)
center_point=center(allPoints)
print(center(allPoints))

space_time_cube=p.gettable(space_time_cube_t)
polygons=[]
for k in space_time_cube:
    add_object = json.loads(k[6])
    polygons.append(add_object)


with open('my_file.csv', mode='w') as csv_file:
    fieldnames = ['tempature', 'pressure', 'humidity','cloud','wind_spped','traffic','trip_time']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(96):
        total_traffic=0
        if (data[0]["start_time_obj"]>=start_datee and data[0]["start_time_obj"]<=start_datee+add_time):
            while True:
                send_date1=start_datee.strftime('%Y-%m-%d %H:%M:%S')
                send_date2=(start_datee+add_time).strftime('%Y-%m-%d %H:%M:%S')
                points=p.getVesselSpecificTime(table_name,default_mmsi,send_date1,send_date2)
                if(len(points)>0):
                    #print(center(points))
                    lon=points[0][0]
                    lat=points[0][1]
                    point1 = point([float(lon), float(lat)])
                    for t in range(len(polygons)):
                        inPolygon=p.pointinpolygon(point1,polygons[t])
                        if inPolygon:
                            own_x=math.ceil((t+1)/border)
                            own_y=(t+1)%border
                            traffic=p.findTraffic(space_time_cube_t,send_date1,send_date2,own_x,own_y,border)
                            total_traffic=total_traffic+traffic
                            break
                start_datee = start_datee+add_time
                if data[0]["finish_time_obj"]<=start_datee:
                    break
            break
        else:
            start_datee = start_datee+add_time

    #write CSV
    print(total_traffic)
    #writer.writerow({'tempature': 10, 'pressure': 50, 'humidity': 30,'cloud': 30,'wind_spped': 30,'traffic': 30,'trip_time':50})
'''
url="http://history.openweathermap.org/data/2.5/history/city?lat="+str(30)+"&lon="+str(30)+"&start="+"1607547600"+"&end="+"1607547600"+"&appid="+appid

response = requests.get(url)
print(response.status_code, response.reason)
print(response.text)
'''


