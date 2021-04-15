from trajectory import *
from datetime import time
from datetime import datetime
from datetime import timedelta
#from pyproj import Proj, transform



f = open("database.txt", "r")
database=f.readline().rstrip("\n")
user=f.readline().rstrip("\n")
password=f.readline().rstrip("\n")
host=f.readline().rstrip("\n")
port=f.readline().rstrip("\n")
p = postgres(database, user,password,host,port)

def copyfiles(i):
  file_name=20201201
  file_name=file_name+i
  print(file_name)
  res=p.copy_files(str(file_name))
  if res==True:
      if(i!=30):
        i=i+1
        copyfiles(i)

copyfiles(0)
    
