CREATE DATABASE plantCare;

CREATE USER plant_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE plantCare TO plant_admin;
