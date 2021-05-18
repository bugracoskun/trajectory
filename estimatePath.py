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

# ANALYSE

points=p.getVesselSpecificTime(table_name,mmsi,epoch1,epoch2)
print(len(points))
print(points[0])

with open('allPoints.csv', mode='w') as csv_file:
    possible_outlers_fieldnames = ['lat','lon']
    writer = csv.DictWriter(csv_file, fieldnames=possible_outlers_fieldnames)
    writer.writeheader()
    for poi in points:
        writer.writerow({'lat':poi[1],'lon':poi[0] })
