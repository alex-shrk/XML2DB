CREATE DATABASE "3dScene"
  WITH OWNER = postgres
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'Russian_Russia.1251'
       LC_CTYPE = 'Russian_Russia.1251'
       CONNECTION LIMIT = -1;
	   
CREATE SEQUENCE public.sec_id_file
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 1
  CACHE 1;
ALTER TABLE public.sec_id_file
  OWNER TO postgres;
  
CREATE TABLE public.faces
(
  id_file integer,
  x1 real,
  y1 real,
  z1 real,
  x2 real,
  y2 real,
  z2 real,
  x3 real,
  y3 real,
  z3 real,
  id_mat text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.faces
  OWNER TO postgres;
  
CREATE TABLE public.objects
(
  id_file integer,
  x real,
  y real,
  z real,
  qw real,
  qx real,
  qy real,
  qz real,
  id_obj text
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.objects
  OWNER TO postgres;
