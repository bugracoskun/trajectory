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

# database connection
f = open("database.txt", "r")
database=f.readline().rstrip("\n")
user=f.readline().rstrip("\n")
password=f.readline().rstrip("\n")
host=f.readline().rstrip("\n")
port=f.readline().rstrip("\n")
p = postgres(database, user,password,host,port)


table_name="ships_1012_geom"
space_time_cube_t="space_time_cube_10_12_2020_219005068"
default_mmsi=219005068
start_datee=datetime(2020,12,10, 00, 00, 00, 00)
start_epoch=math.ceil(datetime(2020,12,10, 00, 00, 00, 00).timestamp())
add_time = timedelta(minutes=15)
border=5
time_range=timedelta(minutes=10)

# ------ Analyse -------------------

f2 = open("trajectory_ships_20min_219005068_local.txt", "r")
data=[]
for x in f2:
    line=x.split()
    mmsi=line[0]
    if mmsi==str(default_mmsi):
        datee=line[2]
        datee=datee.split("-")
        start_time=line[3].split(":")
        finish_time=line[5].split(":")
        finish_epoch=datetime(int(datee[0]),int(datee[1]),int(datee[2]),int(finish_time[0]),int(finish_time[1]),int(finish_time[2]))
        epoch1=datetime(int(datee[0]),int(datee[1]),int(datee[2]),int(start_time[0]),int(start_time[1]),int(start_time[2]))
        epoch2=epoch1+time_range
        while True:
            print(epoch1)
            print(epoch2)
            # get points 
            points=p.getVesselSpecificTime(table_name,mmsi,epoch1,epoch2)
            
            ##transform_coords=p.transformCoords('epsg:4326','epsg:2163',points)
            cluster_result=p.clusterPoints(points,0.5,8)
            print(cluster_result)

            epoch1=epoch2
            epoch2=epoch1+time_range
            if(epoch1>finish_epoch):
                break
        break
        '''
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
        '''

'''
all_date1=start_datee.strftime('%Y-%m-%d %H:%M:%S')
allPoints=p.getVesselAllLoc(table_name,default_mmsi)
center_point=center(allPoints)
print(len(data))

space_time_cube=p.gettable(space_time_cube_t)
polygons=[]
for k in space_time_cube:
    add_object = json.loads(k[6])
    polygons.append(add_object)

print(data)
'''

'''
with open('my_file.csv', mode='w') as csv_file:
    fieldnames = ['tempature', 'pressure', 'humidity','cloud','wind_spped','traffic','trip_time']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for d in range(len(data)):
        start_datee=datetime(2020,12,10, 00, 00, 00, 00)
        for i in range(96):
            total_traffic=0
            if (data[d]["start_time_obj"]>=start_datee and data[d]["start_time_obj"]<=start_datee+add_time):
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
                    if data[d]["finish_time_obj"]<=start_datee:
                        break
                break
            else:
                start_datee = start_datee+add_time

        # get Weather 
        url="http://history.openweathermap.org/data/2.5/history/city?lat="+str(round(center_point['geometry']['coordinates'][1],4))+"&lon="+str(round(center_point['geometry']['coordinates'][0],4))+"&start="+str(start_epoch)+"&end="+str(data[d]["epoch"])+"&appid="+appid
        
        response = requests.get(url)
        if(response.status_code==200):
            weather_data=json.loads(response.text)
            if(weather_data):
                weather_data=weather_data['list'][-1]
                writer.writerow({'tempature': weather_data["main"]["temp"], 'pressure': weather_data["main"]["pressure"], 'humidity': weather_data["main"]["humidity"],'cloud': weather_data["clouds"]["all"],'wind_spped': weather_data["wind"]["speed"],'traffic': total_traffic,'trip_time':data[d]["trip_time"]})
            else:
                #write CSV
                writer.writerow({'tempature': -1, 'pressure': -1, 'humidity': -1,'cloud': -1,'wind_spped': -1,'traffic': -1,'trip_time':data[d]["trip_time"]})
        else:
            print(response.status_code, response.reason)
            writer.writerow({'tempature': -1, 'pressure': -1, 'humidity': -1,'cloud': -1,'wind_spped': -1,'traffic': -1,'trip_time':data[d]["trip_time"]})
        
    
'''