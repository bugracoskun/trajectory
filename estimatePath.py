from trajectory import *
import csv

# database connection
f = open("database.txt", "r")
database=f.readline().rstrip("\n")
user=f.readline().rstrip("\n")
password=f.readline().rstrip("\n")
host=f.readline().rstrip("\n")
port=f.readline().rstrip("\n")
p = postgres(database, user,password,host,port)

# INPUTS
table_name="ships"
epoch1="2020-12-01 00:00:00"
epoch2="2020-12-31 24:00:00"
mmsi="219005068"
input_txt_file="trajectory_ships_20min_219005068_local.txt"

# ANALYSE

f2 = open(input_txt_file, "r")
data=[]
for x in f2:
    line=x.split()
    mmsi=line[0]

    start_time=line[2]+" "+line[3]

    finish_time2=line[4]+" "+line[5]
    print(start_time)
    points=p.getVesselSpecificTime(table_name,mmsi,start_time,finish_time2)
    transform_coords=p.transformCoords('epsg:4326','epsg:2163',points)
    data=data+transform_coords

print(len(data))
print(data[0])

with open('allPoints.csv', mode='w') as csv_file:
    possible_outlers_fieldnames = ['lat','lon']
    writer = csv.DictWriter(csv_file, fieldnames=possible_outlers_fieldnames)
    writer.writeheader()
    for poi in data:
        writer.writerow({'lat':poi[1],'lon':poi[0] })
