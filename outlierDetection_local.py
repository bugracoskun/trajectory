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


table_name="ships"
space_time_cube_t="space_time_cube_219005068"
default_mmsi=219005068
start_datee=datetime(2020,12,1, 00, 00, 00, 00)
start_epoch=math.ceil(datetime(2020,12,1, 00, 00, 00, 00).timestamp())
add_time = timedelta(minutes=15)
border=5
time_range=timedelta(minutes=10)

# ------ Analyse -------------------
analyse_points={} # points will be saved

f2 = open("trajectory_ships_20min_219005068_local.txt", "r")
data=[]
for x in f2:
    line=x.split()
    mmsi=line[0]
    if mmsi==str(default_mmsi):
        datee=line[2]
        datee=datee.split("-")
        start_time=line[3].split(":")
        start_time2=line[2]+" "+line[3]
        general_start_time_obj=datetime(int(datee[0]),int(datee[1]),int(datee[2]),int(start_time[0]),int(start_time[1]),int(start_time[2]))

        finish_time=line[5].split(":")
        finish_time2=line[4]+" "+line[5]
        finish_epoch=datetime(int(datee[0]),int(datee[1]),int(datee[2]),int(finish_time[0]),int(finish_time[1]),int(finish_time[2]))
        epoch1=datetime(int(datee[0]),int(datee[1]),int(datee[2]),int(start_time[0]),int(start_time[1]),int(start_time[2]))
        epoch2=epoch1+time_range

        count=0
        while True:
            print("--------------------")
            print(epoch1)
            print(epoch2)
            # get points 
            points=p.getVesselSpecificTime(table_name,mmsi,epoch1,epoch2)
            points_info=p.getVesselSpecificTimewithTimeInfo(table_name,mmsi,epoch1,epoch2)
            
            if("info"+str(count+1) in analyse_points):
                analyse_points["info"+str(count+1)]=analyse_points["info"+str(count+1)]+points_info
            else:
                analyse_points["info"+str(count+1)]=points_info

            if(str(count+1) in analyse_points):
                analyse_points[str(count+1)]=analyse_points[str(count+1)]+points
            else:
                analyse_points[str(count+1)]=points
            #center
            center_point=center(points)
            
            '''
            # transform (if is needed)
            ##transform_coords=p.transformCoords('epsg:4326','epsg:2163',points)

            # cluster
            cluster_result=p.clusterPoints(points,0.5,8)
            print(cluster_result)
            '''

            epoch_start=datetime(int(datee[0]),int(datee[1]),int(datee[2]),int(start_time[0]),int(start_time[1]),int(start_time[2])).timestamp()
            epoch_finish=datetime(int(datee[0]),int(datee[1]),int(datee[2]),int(finish_time[0]),int(finish_time[1]),int(finish_time[2])).timestamp()
            epoch_res=math.ceil((epoch_start+epoch_finish)/2)

            local_start_time=epoch1.strftime('%Y-%m-%d %H:%M:%S')
            
            time_data=p.getVesselTimeDiff(table_name,default_mmsi,epoch1,epoch2)
            if(len(time_data)>0):
                if(epoch2>finish_epoch):
                    local_finish_time=finish_epoch.strftime('%Y-%m-%d %H:%M:%S')
                    local_finish_time_obj=finish_epoch
                    local_time_trip=round((local_finish_time_obj-epoch1).total_seconds()/60,2)
                else:
                    local_finish_time=time_data[-1][0].strftime('%Y-%m-%d %H:%M:%S')
                    local_finish_time_obj=time_data[-1][0]
                    local_time_trip=round((local_finish_time_obj-epoch1).total_seconds()/60,2)

            data.append(dict({"epoch":epoch_res,"general_start_time":start_time2,"general_start_time_obj":general_start_time_obj,"local_start_time":local_start_time,"local_start_time_obj":epoch1,"general_finish_time_obj":finish_epoch,"general_finish_time":finish_time2,"local_finish_time_obj":local_finish_time_obj,"local_finish_time":local_finish_time,"total_trip_time":line[6],"local_time_trip":local_time_trip,"center":center_point}))

            epoch1=epoch2
            epoch2=epoch1+time_range
            if(epoch1>finish_epoch):
                break
            else:
                count=count+1
        #break

#print(data)
#print(analyse_points)

analyse_number=0
possible_outliers=[]

while True:
    if(str(analyse_number+1) in analyse_points):
        # cluster
            cluster_result=p.clusterPoints(analyse_points[str(analyse_number+1)],0.3,40)
            #print(cluster_result)
            for out in range(len(cluster_result)):
                if cluster_result[out]==-1:
                    possible_outliers.append(dict({"part":analyse_number+1,"point":analyse_points["info"+str(analyse_number+1)][out]}))
            analyse_number=analyse_number+1
    else:
        break


print(possible_outliers)
print(len(possible_outliers))
with open('possible_outliers.csv', mode='w') as csv_file:
    possible_outlers_fieldnames = ['part','time', 'lat', 'lon']
    writer = csv.DictWriter(csv_file, fieldnames=possible_outlers_fieldnames)
    writer.writeheader()
    for poss_outlier in possible_outliers:
        writer.writerow({'part':poss_outlier["part"],'time': poss_outlier["point"][2],'lat':poss_outlier["point"][1],'lon':poss_outlier["point"][0] })

'''
all_date1=start_datee.strftime('%Y-%m-%d %H:%M:%S')

#allPoints=p.getVesselAllLoc(table_name,default_mmsi)

# get space time cube data
space_time_cube=p.gettable(space_time_cube_t)
polygons=[]
for k in space_time_cube:
    add_object = json.loads(k[6])
    polygons.append(add_object)
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