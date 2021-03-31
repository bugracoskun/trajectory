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



result=p.gettable('space_time_cube_10_12_2020_219005068')
print(len(result))
print(result[0])

new_val=1

for i in range(len(result)):
    if i%5==0 and i!=0:
        new_val=new_val+1
        if new_val==6:
            new_val=1
        p.updateColumn('space_time_cube_10_12_2020_219005068',new_val,result[i][0])
    else:
        p.updateColumn('space_time_cube_10_12_2020_219005068',new_val,result[i][0])
#p.updateColumn('space_time_cube_10_12_2020_219005068',1)

