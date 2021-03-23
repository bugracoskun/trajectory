from turf.square_grid import square_grid
from turf.boolean_point_in_polygon import boolean_point_in_polygon
from turf import point
from turf.bbox import bbox
import json
import psycopg2
from datetime import datetime
from trajectory import *

# database connection
f = open("database.txt", "r")
database=f.readline().rstrip("\n")
user=f.readline().rstrip("\n")
password=f.readline().rstrip("\n")
host=f.readline().rstrip("\n")
port=f.readline().rstrip("\n")
p = postgres(database, user,password,host,port)

cur = p.conn.cursor()

# Usage Data
data='{\
       "bbox_area":[10.69, 57.40 ,11.53, 57.85],\
       "cell_side":5,\
       "unit":"kilometers",\
       "table":"ships_1012_geom"\
      }'
data = json.loads(data)


#define grids
bbox_area = data["bbox_area"]
cellSide = data["cell_side"]
options = "{units: "+data["unit"]+"}"

squareGrid = square_grid(bbox_area, cellSide, options)

for i in range(len(squareGrid["features"])):
    bbox_feat=bbox(squareGrid["features"][i])
    
    # get points in bbox and date
    trips=p.get_points_bbox(data["table"],bbox_feat,'2020-12-10 00:00:00','2020-12-10 00:15:00')
    print(trips)


# Yöntem 2
'''
trips_list=[]
for trip in trips:
    mmsi=trip[0]
    query2 =  "SELECT lat,lon "\
    "from ships_1012_geom "\
    "where mmsi={} "\
    "limit 1 ".format(mmsi)

    cur.execute(query2)
    result = cur.fetchall()
    for res in result:
        lat=res[0]
        lon=res[1]
        point1 = point([lon, lat])
        for i in range(len(squareGrid)):
            point_in_poly=boolean_point_in_polygon(point1, squareGrid["features"][i])
            print(point_in_poly)
print(len(trips))
'''

cur.close()
p.conn.close()