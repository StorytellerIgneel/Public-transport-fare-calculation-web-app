-- CREATE DATABASE TCPIPNAD; only works for psql or mysql
-- USE TCPIPNAD;

CREATE TABLE if not EXISTS fares(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin_station VARCHAR(255) NOT NULL,
    destination_station VARCHAR(255) NOT NULL,
    fare DECIMAL(10, 2) NOT NULL
)

\copy fares(origin_station, destination_station, fare) 
FROM 'src\components\backend\db_scripts\Fare_melted.csv' 
DELIMITER ',' 
CSV HEADER;

CREATE TABLE if not EXISTS times(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin_station VARCHAR(255) NOT NULL,
    destination_station VARCHAR(255) NOT NULL,
    travel_time INTEGER NOT NULL
)

\copy times(origin_station, destination_station, travel_time) 
FROM 'src\components\backend\db_scripts\Time_melted.csv' 
DELIMITER ',' 
CSV HEADER;