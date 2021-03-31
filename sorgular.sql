create extension postgis; 
-- text 
CREATE TABLE ships (
  "id" SERIAL,
  time_info timestamp,
  Type_of_mobile text,
  MMSI text,
  lat text,
  lon text,
  nav_status text,
  ROT text,
  SOG text,
  COG text,
  heading text,
  IMO text,
  callsign text,
  name_vessel text,
  ship_type text,
  cargo_type text,
  width text,
  len text,
  position_fixed_device text,
  draught text,
  destination text,
  eta text,
  data_source_type text,
  size_a text,
  size_b text,
  size_c text,
  size_d text,
  PRIMARY KEY ("id")
)
-- optimal table
CREATE TABLE ships_opt_17_12 (
  "id" SERIAL,
  time_info timestamp,
  Type_of_mobile character varying(50),
  MMSI BIGINT,
  lat double precision,
  lon double precision,
  nav_status character varying(50),
  ROT double precision,
  SOG double precision,
  COG double precision,
  heading int,
  IMO text,
  callsign character varying(50),
  name_vessel text,
  ship_type character varying(50),
  cargo_type text,
  width int,
  len int,
  position_fixed_device character varying(50),
  draught double precision,
  destination character varying(40),
  eta timestamp,
  data_source_type character varying(50),
  size_a int,
  size_b int,
  size_c int,
  size_d int,
  PRIMARY KEY ("id")
)
-- geom table
CREATE TABLE ships_1712_geom (
  "id" SERIAL,
  time_info timestamp,
  Type_of_mobile character varying(50),
  MMSI BIGINT,
  lat double precision,
  lon double precision,
  nav_status character varying(50),
  ROT double precision,
  SOG double precision,
  COG double precision,
  heading int,
  IMO text,
  callsign character varying(50),
  name_vessel text,
  ship_type character varying(50),
  cargo_type text,
  width int,
  len int,
  position_fixed_device character varying(50),
  draught double precision,
  destination character varying(40),
  eta timestamp,
  data_source_type character varying(50),
  size_a int,
  size_b int,
  size_c int,
  size_d int,
  geom geometry(point, 4326),
  PRIMARY KEY ("id")
)

select *
from ships_opt_17_12
limit 5

insert into ships_1712_geom(id, time_info, Type_of_mobile, MMSI, lat, 
		        lon, nav_status, ROT, SOG, COG, 
		        heading, IMO, callsign, name_vessel, ship_type, cargo_type, 
		        width, len, position_fixed_device, draught, 
		        destination, eta, data_source_type, size_a, size_b, size_c, size_d,geom)
	select id, time_info, Type_of_mobile, MMSI, lat, 
		        lon, nav_status, ROT, SOG, COG, 
		        heading, IMO, callsign, name_vessel, ship_type, cargo_type, 
		        width, len, position_fixed_device, draught, 
		        destination, eta, data_source_type, size_a, size_b, size_c, size_d,
				ST_SetSRID(ST_Point(lon,lat),4326)
	from ships_opt_17_12

select *
from ships_1712_geom
limit 10

select *
from ships_1404_geom
where ship_type='Passenger'
limit 10

select DISTINCT mmsi
from ships_1012_geom
where ship_type='Passenger' and mmsi=211445190

--???????
select *
from ships
where mmsi='219006386' and time_info<'2020-04-13 20:00:00' and time_info>'2020-04-13 9:00:00'
order by time_info desc
limit 1000

--209864000
--211245200 (Güzel veri)
--219003141 (veri2)
-- 219012639 (Duran gemi)
-- 265810550 (Çok kısa yolculuk. Gemi durmuyor gibi)
select *
from ships_geom
where mmsi='219012639'
order by time_info desc

select *
from ships
where mmsi='211190000' and time_info<'2020-04-14 00:00:00' and time_info>'2020-04-13 00:00:00' and rot='0.0' and sog='0.0'
order by time_info asc

select mmsi,count(*)
from ships
where ship_type='Passenger'
group by mmsi
limit 100

select ship_type,count(*)
from ships
group by ship_type

select *
from zones
limit 10

select *
from ships_geom
limit 10

--Point in polygon
SELECT z1.gid
FROM ships_geom s
FULL JOIN zones z1 ON ST_Contains(z1.geom, s.geom)
WHERE s.id = 1

SELECT z1.gid
FROM ships_geom s
FULL JOIN zones z1 ON ST_Contains(ST_Buffer(z1.geom,100), s.geom)
WHERE s.id = 1

-- st_Dwithin unit: degrees or radian


SELECT *
FROM ships_1012_geom s
FULL JOIN zones z1 ON ST_Dwithin(z1.geom, s.geom,0.003)
WHERE s.mmsi = 211379770 and z1.geom!='' and sog<0.5
order by time_info

select *
from ships_geom
where mmsi = 211245200 and sog<0.5
order by time_info

--14.04 fark
SELECT (t2.time_info - t1.time_info) AS diff
FROM ships_1404_geom t1 Full JOIN ships_1404_geom t2 ON t1.id=t2.id
WHERE t1.mmsi = 211245200 and t1.sog<0.3 and t2.mmsi = 211245200 and t2.sog<0.3

--14.04
SELECT *
FROM ships_1404_geom s
FULL JOIN zones z1 ON ST_Dwithin(z1.geom, s.geom,0.003)
WHERE s.mmsi = 211245200 and sog<0.3
order by time_info

--15.04
SELECT *
FROM ships_1012_geom s
WHERE s.mmsi = 311000929                     
order by time_info

SELECT count(*)
FROM ships_opt_10_12
where ship_type='Passenger'
group by MMSI

SELECT *
FROM ships_opt_10_12
limit 10

--219006221
--265509950: farklı durakları olan gemi 
--211440340: hatalı veri
--219016938: güzergah farkları
--211727510: 2 saatlik yolculuk

select *
from zones
where cntr_code='DE'


SELECT *
FROM ships_geom s
FULL JOIN zones z1 ON ST_Dwithin(ST_Transform(z1.geom,2163), ST_Transform(s.geom,2163),10)
WHERE s.mmsi = 211245200 and z1.geom!=''

SELECT *
FROM ships_geom s
FULL JOIN zones z1 ON ST_Dwithin(z1.geom, s.geom,0.0001)
WHERE s.id = 1

--12.10
SELECT *
FROM ships_1012_geom s
FULL JOIN zones z1 ON ST_Dwithin(z1.geom, s.geom,0.003)
WHERE s.mmsi = 211445190 and z1.geom!='' and sog<0.4
order by time_info

SELECT *
FROM ships_1012_geom s
WHERE s.mmsi = 219005068    
order by time_info

--Point Buffer

-- saat 05.04
SELECT *
FROM ships_1012_geom s
FULL JOIN zones z1 ON ST_Dwithin(z1.geom, s.geom,0.001)
WHERE s.mmsi = 211245200 and z1.geom!='' and sog<0.4 and lat=54.146222 and lon=12.097805
order by time_info

-- saat 12.15
SELECT *
FROM ships_1012_geom s
FULL JOIN zones z1 ON ST_Dwithin(z1.geom, s.geom,0.002)
WHERE s.mmsi = 211245200 and z1.geom!='' and sog<0.4 and lat=55.366553 and lon=13.154577
order by time_info

--epoch oluşturuldu
select time_info,date_part('epoch', time_info) from ships_1012_geom limit 5;

ALTER TABLE ships_1012_geom
ADD epoch text;

Update ships_1012_geom t1
set epoch = (select date_part('epoch', time_info) from ships_1012_geom t2 where t1.id=t2.id);

-- geom yeni
ALTER TABLE ships_1012_geom
ADD geom2 geometry(point,32632);

ALTER TABLE ships_1012_geom   
DROP COLUMN geom2;  

select *
from ships_1012_geom
where lat>90
limit 5

select *
from ships_1012_geom
where lat<-90

select *
from ships_1012_geom
limit 5

--32632
Update ships_1012_geom t1
set geom2 = (select ST_transform(t2.geom,32632) from ships_1012_geom t2 where t1.id=t2.id and t2.lat<=90 and t2.lat>=-90 and t2.lon>=-180 and t2.lon<=180);

select st_transform(ST_SetSRID(ST_Point(-100,-80),4326),3857)

-- olmaması gereken veriler
select count(*)
from ships_1012_geom
where lat<-90 or lat>90 or lon<-180 or lon>180

--veri hakkında bilgi
select count(*)
from ships_1012_geom

select count(*)
from ships_1012_geom
where ship_type='Passenger'

select mmsi
from ships_1012_geom
where time_info>='2020-12-10 00:15:00' and time_info<='2020-12-10 00:30:00'
group by mmsi

-- Get Points in bbox
SELECT mmsi
from ships_1012_geom
where geom && ST_MakeEnvelope(11.10499, 55.14280 ,11.26270, 55.23284, 4326) and time_info>='2020-12-10 00:00:00' and time_info<='2020-12-10 24:00:00'
group by mmsi

-- space time cube
CREATE TABLE space_time_cube_10_12_2020_219005068 (
  "id" SERIAL,
  time_start timestamp,
  time_finish timestamp,
  x int,
  y int,
  counts int,
  PRIMARY KEY ("id")
)

INSERT INTO space_time_cube_10_12_2020(time_start,time_finish,x,y,counts)
VALUES ('2020-04-14 00:00:00','2020-04-14 00:15:00',3,5,5);

---- SPACE TIME CUBE

-- 5  den büyük değerler
select *
from space_time_cube_10_12_2020
where counts>5

-----------------------

--0.001 => 111m

-- Kaynaklar
--https://stackoverflow.com/questions/8444753/st-dwithin-takes-parameter-as-degree-not-meters-why
--https://gis.stackexchange.com/questions/221978/st-dwithin-calc-meters-transform-or-cast
--https://www.usna.edu/Users/oceano/pguth/md_help/html/approx_equivalents.htm#:~:text=1%C2%B0%20%3D%20111%20km%20(or,0.001%C2%B0%20%3D111%20m

--Zones
-- https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/lau#lau19