from trajectory import *
from datetime import time
from datetime import datetime

datee='2020-12-10 00:00:00'
b = datetime(2020, 12, 10, 00, 00, 00, 00)

c=b.strftime('%m-%d-%Y %H:%M:%S')
print(c)

f = open("database.txt", "r")
database=f.readline().rstrip("\n")
user=f.readline().rstrip("\n")
password=f.readline().rstrip("\n")
host=f.readline().rstrip("\n")
port=f.readline().rstrip("\n")
p = postgres(database, user,password,host,port)

adddatabase=p.addSTCDatabase('space_time_cube_10_12_2020','2020-12-10 00:00:00','2020-12-10 00:15:00',0,0,10)
