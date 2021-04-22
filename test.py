from datetime import datetime
from datetime import timedelta
deneme={
    "day1":[(34,45),(2,2)],
    "day2":[(35,35),(3,3)]
}

print(deneme["day1"])

deneme["day3"]=[(10,10),(20,20)]

if("day4" in deneme):
    print(deneme["day4"])
else:
    print("yok")

print(timedelta(minutes=10)*3)