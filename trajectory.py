# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 14:46:34 2020

@author: Bugra

Kütüphane ve fonksiyonlar burada yazılıyor.

1) init --> postgres bağlantısı sağlanır.
2) find_seaport --> Verilen gün ve saatte buffera göre geminin konumlarını bulur
3) get_points_bbox --> verilen gün,zaman ve bboxta yer alan gemilerin mmsi değerleri döndürülür
"""

import psycopg2
from datetime import datetime
from datetime import timedelta
from turf.square_grid import square_grid
from turf.boolean_point_in_polygon import boolean_point_in_polygon
from turf.bbox import bbox
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from pyproj import Proj, transform
#import os

class postgres():
    def __init__(self, dbName, userName, pswd, host, port):
        try:
            self.conn = psycopg2.connect(database=dbName,
                            user=userName,
                            password=pswd,
                            host=host,
                            port=port)
            print("Connected to PostgreSQL Server")
        except:
            print("Postgres connection failed!")

# dosyaları tabloya kopyalama
    def copy_files(self,file_name):
        cur = self.conn.cursor()
        query = "copy public.ships_opt (time_info, type_of_mobile, mmsi, lat, lon, nav_status, rot, sog, cog, heading, imo, callsign, name_vessel, ship_type, cargo_type, width, len, position_fixed_device, draught, destination, eta, data_source_type, size_a, size_b, size_c, size_d) "\
                "FROM 'D:/trajectory/aisdk_{}.csv' "\
                "CSV HEADER QUOTE '\"' ESCAPE ''''".format(file_name)

        cur.execute(query)
        self.conn.commit()
        return True

# Verilen gün ve saatte buffera göre geminin konumlarını bulur
    def find_seaport(self,day,mmsi,sog,buffer):
        cur = self.conn.cursor()
        query = "SELECT * " \
                "FROM ships_{}_geom s " \
                "FULL JOIN zones z1 ON ST_Dwithin(z1.geom, s.geom,{})" \
                "WHERE s.mmsi = {} and sog<{}" \
                "ORDER BY time_info ".format(day, buffer, mmsi, sog)

        cur.execute(query)
        rows = cur.fetchall()
        result = []
        
        for row in rows:
            result.append(row)
            
        cur.close()
        
        return result
    
# verilen gün ve bbox ta yer alan gemi sayısını bulur
    def get_points_bbox(self,table_name,bbox_feat,time_start,time_finish):
        # st_makeenvelope --> float xmin, float ymin, float xmax, float ymax
        query =  "SELECT mmsi "\
        "from {} "\
        "where geom && ST_MakeEnvelope({}, {} ,{}, {}, 4326) and time_info>='{}' and time_info<='{}' "\
        "group by mmsi ".format(table_name,bbox_feat[0],bbox_feat[1],bbox_feat[2],bbox_feat[3],time_start,time_finish)

        cur = self.conn.cursor()
        cur.execute(query)
        trips=cur.fetchall()
        return trips

# get vessel on mmsi
    def getVessel(self,table_name,mmsi):
        query =  "SELECT * "\
        "from {} "\
        "where mmsi='{}' ".format(table_name,mmsi)

        cur = self.conn.cursor()
        cur.execute(query)
        result=cur.fetchall()
        return result

# space time cube add to database
    def addSTCDatabase(self,table_name,time_start,time_finish,x,y,counts,feature):
        query =  "INSERT INTO {}(time_start,time_finish,x,y,counts,feature) "\
        "VALUES ('{}','{}',{},{},{},'{}') ".format(table_name,time_start,time_finish,x,y,counts,feature)

        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        return True

# change char in string
    def replace(self,s, position, character):
        return s[:position] + character + s[position+1:]

# update column
    def updateColumn(self,table_name,value,id):
        query='UPDATE {} ' \
              'SET x = {} ' \
              'WHERE id= {}'.format(table_name,value,id)

        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        return True

# get table
    def gettable(self,table_name):
        query='select * ' \
              'from {}' \
              ' order by id'.format(table_name)

        cur = self.conn.cursor()
        cur.execute(query)
        result=cur.fetchall()
        return result
    
# Find traffic
    def findTraffic(self,table_name,time_start,time_finish,x,y,bounds):
        count=0
        query =  "SELECT counts "\
        "from {} "\
        "where x={} and y={} and time_start='{}' and time_finish>= '{}' ".format(table_name,x,y,time_start,time_finish)

        cur = self.conn.cursor()
        cur.execute(query)
        result=cur.fetchall()
        new_count=result[0][0]
        count=count+new_count

        if x+1<bounds:
            query =  "SELECT counts "\
            "from {} "\
            "where x={} and y={} and time_start='{}' and time_finish>= '{}' ".format(table_name,x+1,y,time_start,time_finish)

            cur = self.conn.cursor()
            cur.execute(query)
            result=cur.fetchall()
            new_count=result[0][0]
            count=count+new_count
        if x-1>0:
            query =  "SELECT counts "\
            "from {} "\
            "where x={} and y={} and time_start='{}' and time_finish>= '{}' ".format(table_name,x-1,y,time_start,time_finish)

            cur = self.conn.cursor()
            cur.execute(query)
            result=cur.fetchall()
            new_count=result[0][0]
            count=count+new_count

        if y+1<bounds:
            query =  "SELECT counts "\
            "from {} "\
            "where x={} and y={} and time_start='{}' and time_finish>= '{}' ".format(table_name,x,y+1,time_start,time_finish)

            cur = self.conn.cursor()
            cur.execute(query)
            result=cur.fetchall()
            new_count=result[0][0]
            count=count+new_count

        if y-1>0:
            query =  "SELECT counts "\
            "from {} "\
            "where x={} and y={} and time_start='{}' and time_finish>= '{}' ".format(table_name,x,y-1,time_start,time_finish)

            cur = self.conn.cursor()
            cur.execute(query)
            result=cur.fetchall()
            new_count=result[0][0]
            count=count+new_count

        if x+1<bounds and y+1<bounds:
            query =  "SELECT counts "\
            "from {} "\
            "where x={} and y={} and time_start='{}' and time_finish>= '{}' ".format(table_name,x+1,y+1,time_start,time_finish)

            cur = self.conn.cursor()
            cur.execute(query)
            result=cur.fetchall()
            new_count=result[0][0]
            count=count+new_count

        if x+1<bounds and y-1>0:
            query =  "SELECT counts "\
            "from {} "\
            "where x={} and y={} and time_start='{}' and time_finish>= '{}' ".format(table_name,x+1,y-1,time_start,time_finish)

            cur = self.conn.cursor()
            cur.execute(query)
            result=cur.fetchall()
            new_count=result[0][0]
            count=count+new_count

        if x-1>0 and y+1<bounds:
            query =  "SELECT counts "\
            "from {} "\
            "where x={} and y={} and time_start='{}' and time_finish>= '{}' ".format(table_name,x-1,y+1,time_start,time_finish)

            cur = self.conn.cursor()
            cur.execute(query)
            result=cur.fetchall()
            new_count=result[0][0]
            count=count+new_count

        if x-1>0 and y-1>0:
            query =  "SELECT counts "\
            "from {} "\
            "where x={} and y={} and time_start='{}' and time_finish>= '{}' ".format(table_name,x-1,y-1,time_start,time_finish)

            cur = self.conn.cursor()
            cur.execute(query)
            result=cur.fetchall()
            new_count=result[0][0]
            count=count+new_count

        return count

# create Grids
    def createGrids(self,bbox_area, cellSide, options):
        squareGrid = square_grid(bbox_area, cellSide, options)
        return squareGrid

# point in polygon
    def pointinpolygon(self,point,polygon):
        result = boolean_point_in_polygon(point, polygon)
        return result
    
# get vessel on mmsi with specific time
    def getVesselSpecificTime(self,table_name,mmsi,start_time,finish_time):
        query =  "SELECT lon,lat "\
        "from {} "\
        "where mmsi='{}' and time_info>= '{}' and time_info<='{}' ".format(table_name,mmsi,start_time,finish_time)

        cur = self.conn.cursor()
        cur.execute(query)
        result=cur.fetchall()
        return result

# get vessel on mmsi with specific time with INFO
    def getVesselSpecificTimewithTimeInfo(self,table_name,mmsi,start_time,finish_time):
        query =  "SELECT lon,lat,time_info "\
        "from {} "\
        "where mmsi='{}' and time_info>= '{}' and time_info<='{}' ".format(table_name,mmsi,start_time,finish_time)

        cur = self.conn.cursor()
        cur.execute(query)
        result=cur.fetchall()
        return result

    def getVesselAllLoc(self,table_name,mmsi):
        query =  "SELECT lon,lat "\
        "from {} "\
        "where mmsi='{}' ".format(table_name,mmsi)

        cur = self.conn.cursor()
        cur.execute(query)
        result=cur.fetchall()
        return result
    
# find polygon bbox
    def find_bbox(self,polygon):
        bbox_result = bbox(polygon)
        return bbox_result

#boolean vessel bbox
    def booleanFindVesselBbox(self,table_name,bbox_feat,time_start,time_finish,mmsi):
        query =  "SELECT mmsi "\
        "from {} "\
        "where geom && ST_MakeEnvelope({}, {} ,{}, {}, 4326) and time_info>='{}' and time_info<='{}' and mmsi={}"\
        "group by mmsi ".format(table_name,bbox_feat[0],bbox_feat[1],bbox_feat[2],bbox_feat[3],time_start,time_finish,mmsi)

        cur = self.conn.cursor()
        cur.execute(query)
        trips=cur.fetchall()
        if len(trips)==1:
            return True
        else:
            return False
    
#get a table
    def gettable(self,table_name):
        query =  "SELECT * "\
        "from {} ".format(table_name)

        cur = self.conn.cursor()
        cur.execute(query)
        result=cur.fetchall()
        return result

# get vessel time difference
    def getVesselTimeDiff(self,table_name,mmsi,start_time,end_time):
        query =  "SELECT time_info "\
        "from {} "\
        "where mmsi='{}' and time_info>='{}' and time_info<='{}' "\
        "order by time_info asc ".format(table_name,mmsi,start_time,end_time)

        cur = self.conn.cursor()
        cur.execute(query)
        result=cur.fetchall()
        return result

# cluster Points with dbscan
    def clusterPoints(self,points,epsilon,min_samples):
        X = StandardScaler().fit_transform(points)
        clustering = DBSCAN(eps=epsilon, min_samples=min_samples).fit(X)
        return clustering.labels_

# transform Coordinates
    def transformCoords(self,proj1,proj2,coords):
        transform_coords=[]
        for i in range(len(coords)):
            inProj = Proj(proj1)
            outProj = Proj(proj2)
            x2,y2 = transform(inProj,outProj,coords[i][0],coords[i][1])
            transform_coords.append([x2,y2])
        return transform_coords

# get table for update
    def gettableToUpdate(self,table_name,id):
        query='select id,lat,lon ' \
              'from {} ' \
              'where id={}'.format(table_name,id)

        cur = self.conn.cursor()
        cur.execute(query)
        result=cur.fetchall()
        return result

# upfate geom
    def updateGeom(self,table_name,lon,lat,id):
        query='update {} ' \
              'set geom=ST_SetSRID(ST_Point({},{}),4326) ' \
              'where id={} '.format(table_name,lon,lat,id)

        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        return True

# find time interval
    def findinterval(self,time,file):
        f2 = open(file, "r")
        for x in f2:
            line=x.split()
            mmsi=line[0]
            tripId=line[1]

            datee=line[2]
            datee=datee.split("-")
            start_time=line[3].split(":")
            start_time2=line[2]+" "+line[3]
            general_start_time_obj=datetime(int(datee[0]),int(datee[1]),int(datee[2]),int(start_time[0]),int(start_time[1]),int(start_time[2]))

            finish_time=line[5].split(":")
            finish_time2=line[4]+" "+line[5]
            finish_epoch=datetime(int(datee[0]),int(datee[1]),int(datee[2]),int(finish_time[0]),int(finish_time[1]),int(finish_time[2]))

            if(time>=general_start_time_obj and time<=finish_epoch):
                return tripId
        return False