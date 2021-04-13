from trajectory import *
from datetime import time
from datetime import datetime
from datetime import timedelta
from pyproj import Proj, transform



f = open("database.txt", "r")
database=f.readline().rstrip("\n")
user=f.readline().rstrip("\n")
password=f.readline().rstrip("\n")
host=f.readline().rstrip("\n")
port=f.readline().rstrip("\n")
p = postgres(database, user,password,host,port)



res=p.transformCoords('epsg:3857','epsg:4326',[-11705274.6374,4826473.6922])
print(res)
