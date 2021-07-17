from trajectory import *
import csv

tripid=[]
day=[]
number_of_outliers=0
number_of_day=0

with open('possible_outliers.csv',mode='r') as csv_file2:
    csv_reader = csv.reader(csv_file2, delimiter=',')
    for row in csv_reader:
        if(len(row)!=0 and row[0]!="part"):
            tid=int(row[1])
            dayvalue=row[2].split()
            if(tid not in tripid):
                tripid.append(tid)
            if(dayvalue[0] not in day):
                day.append(dayvalue[0])
#print(tripid)
print("Yolculuk Sayısı:",len(tripid))
#print(day)
print("Toplam Gün:",len(day))