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
    def addSTCDatabase(self,table_name,time_start,time_finish,x,y,counts):
        query =  "INSERT INTO {}(time_start,time_finish,x,y,counts) "\
        "VALUES ('{}','{}',{},{},{}) ".format(table_name,time_start,time_finish,x,y,counts)

        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        return True