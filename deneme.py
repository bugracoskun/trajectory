from trajectory import *
from datetime import time
from datetime import datetime
from datetime import timedelta

datee='2020-12-10 00:00:00'
b = datetime(2020, 12, 10, 00, 00, 00, 00)
d = datetime(2020, 12, 10, 00, 15, 00, 00)

print(d-b>timedelta(minutes=14))

c=b.strftime('%m-%d-%Y %H:%M:%S')

def replace(s, position, character):
    return s[:position] + character + s[position+1:]

x = c.split()
y=x[1]

y=replace(y, 2, '_')
y=replace(y, 5, '_')
"""
f = open("database.txt", "r")
database=f.readline().rstrip("\n")
user=f.readline().rstrip("\n")
password=f.readline().rstrip("\n")
host=f.readline().rstrip("\n")
port=f.readline().rstrip("\n")
p = postgres(database, user,password,host,port)

adddatabase=p.addSTCDatabase('space_time_cube_10_12_2020','2020-12-10 00:00:00','2020-12-10 00:15:00',0,0,10)
"""
