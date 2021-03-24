from turf.square_grid import square_grid
from turf.boolean_point_in_polygon import boolean_point_in_polygon
from turf import point
from turf.bbox import bbox
from turf.center import center
import json
import psycopg2
from datetime import datetime
from geojson import Point, Feature, FeatureCollection, dump
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
       "table":"ships_1012_geom",\
       "table_spaceTimeCube":"space_time_cube_10_12_2020"\
      }'
data = json.loads(data)


#define grids
bbox_area = data["bbox_area"]
cellSide = data["cell_side"]
options = "{units: "+data["unit"]+"}"

squareGrid = square_grid(bbox_area, cellSide, options)
features = []
x=0
y=0
for i in range(len(squareGrid["features"])):
    bbox_feat=bbox(squareGrid["features"][i])
    center_feat=center(squareGrid["features"][i])
    # get points in bbox and date
    trips=p.get_points_bbox(data["table"],bbox_feat,'2020-12-10 00:00:00','2020-12-10 00:15:00')

    # add to geojson
    center_feat["properties"]["count"]=len(trips)
    features.append(center_feat)
    print(center_feat)
    # add to database
    if i%5==0 and i!=0:
        x=x+1
        y=0
    else:
        y=i%5
    adddatabase=p.addSTCDatabase(data["table_spaceTimeCube"],'2020-12-10 00:00:00','2020-12-10 00:15:00',x,y,len(trips))


feature_collection = FeatureCollection(features)
with open('myfile.geojson', 'w') as f:
   dump(feature_collection, f)

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