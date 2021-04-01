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
import datetime
from turf.square_grid import square_grid
from turf.boolean_point_in_polygon import boolean_point_in_polygon
from turf.bbox import bbox
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

