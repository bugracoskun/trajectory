-- optimal table
CREATE TABLE ships_opt_weekly (
  "id" SERIAL,
  time_info timestamp,
  Type_of_mobile character varying(50),
  MMSI BIGINT,
  lat double precision,
  lon double precision,
  nav_status character varying(150),
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

-- Add geom column
ALTER TABLE ships_opt_weekly
ADD COLUMN geom geometry(Geometry,4326);

-- Set geometry column
UPDATE ships_opt_weekly d
SET geom = ST_SetSRID(ST_Point(d.lon,d.lat),4326)