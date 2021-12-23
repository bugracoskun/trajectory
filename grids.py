from trajectory import *
from datetime import datetime
from datetime import timedelta
from turf.square_grid import square_grid
from turf.boolean_point_in_polygon import boolean_point_in_polygon
from turf import point
from turf.bbox import bbox
from turf.center import center
import json
import psycopg2
from geojson import Point, Feature, FeatureCollection, dump

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
# "bbox_area":[10.69, 57.40 ,11.53, 57.85],\
data='{\
       "bbox_area":[11.10499, 55.14280 ,11.26270, 55.23284],\
       "cell_side":2,\
       "unit":"kilometers",\
       "table":"ships_opt",\
       "table_spaceTimeCube":"space_time_cube_219005068",\
       "year":2021,\
       "month":9,\
       "day":1,\
       "time":15,\
       "i":5\
      }'
data = json.loads(data)

#define grids
bbox_area = data["bbox_area"]
cellSide = data["cell_side"]
options = "{units: "+data["unit"]+"}"
squareGrid = square_grid(bbox_area, cellSide, options)

time_range=1440/data["time"]

for newday in range(31):
    #date
    timee = datetime(data["year"], data["month"], data["day"]+newday, 00, 00, 00, 00)
    start_time=timee.strftime('%Y-%m-%d %H:%M:%S')

    add_time =timedelta(minutes=data["time"])
    timee2 = timee+add_time
    finish_time=timee2.strftime('%Y-%m-%d %H:%M:%S')

    '''
    with open('gridss.geojson', 'w') as f:
            dump(squareGrid, f)
    '''

    for j in range(int(time_range)):
        features = []
        x=1
        y=1
        if j!=0:
            new_time=timee+add_time
            timee=new_time
            start_time=new_time.strftime('%Y-%m-%d %H:%M:%S')

            new_finish_time=new_time+add_time
            finish_time=new_finish_time.strftime('%Y-%m-%d %H:%M:%S')
        print(start_time)
        print(finish_time)
        for i in range(len(squareGrid["features"])):
            bbox_feat=bbox(squareGrid["features"][i])
            center_feat=center(squareGrid["features"][i])
            # get points in bbox and date
            trips=p.get_points_bbox(data["table"],bbox_feat,start_time,finish_time)
            # add to geojson
            center_feat["properties"]["count"]=len(trips)
            features.append(center_feat)
            # add to database
            if i%data["i"]==0 and i!=0:
                x=x+1
                y=1
            else:
                y=i%data["i"]+1
            obj = json.dumps(squareGrid["features"][i])
            adddatabase=p.addSTCDatabase(data["table_spaceTimeCube"],start_time,finish_time,x,y,len(trips),obj)
        feature_collection = FeatureCollection(features)
        
        x=start_time.split()
        geojson_name=x[1]
        geojson_name=p.replace(geojson_name, 2, '_')
        geojson_name=p.replace(geojson_name, 5, '_')
        #with open(geojson_name+'.geojson', 'w') as f:
        #    dump(feature_collection, f)

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