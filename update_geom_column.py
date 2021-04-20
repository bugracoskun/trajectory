from trajectory import *
from datetime import time
from datetime import datetime
from datetime import timedelta



f = open("database.txt", "r")
database=f.readline().rstrip("\n")
user=f.readline().rstrip("\n")
password=f.readline().rstrip("\n")
host=f.readline().rstrip("\n")
port=f.readline().rstrip("\n")
p = postgres(database, user,password,host,port)

#"305179692"

for i in range(305179692):
    if(i%1000000==0):
        print(i)
    data=p.gettableToUpdate("ships_opt",i+1)
    idd=data[0][0]
    lat=data[0][1]
    lon=data[0][2]
    p.updateGeom("ships_opt",lon,lat,i+1)
