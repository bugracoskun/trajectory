# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 14:46:34 2020

@author: Bugra

Kütüphane ve fonksiyonlar burada yazılıyor.

1) init --> postgres bağlantısı sağlanır.
2) find_seaport --> Verilen gün ve saatte buffera göre geminin konumlarını bulur
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