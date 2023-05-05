CREATE DATABASE airflow_db;
CREATE USER airflow_user WITH PASSWORD 'airflow_pass';
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;
--USE airflow_db;
--GRANT ALL ON SCHEMA public TO airflow_user;

CREATE DATABASE weather_db;

\c weather_db;

CREATE TABLE city (
	city_id smallint PRIMARY KEY,
	city_name VARCHAR (32) UNIQUE NOT NULL,
    latitude real,
    longitude real,
    timestamp_track timestamp
);

INSERT INTO city (city_id, city_name, latitude, longitude, timestamp_track)
VALUES(1, 'London', 51.51, -0.13, '2015-01-01 00:00:00');

INSERT INTO city (city_id, city_name, latitude, longitude, timestamp_track)
VALUES(2, 'Manchester', 53.48, -2.24, '2015-01-01 00:00:00');

INSERT INTO city (city_id, city_name, latitude, longitude, timestamp_track)
VALUES(3, 'Liverpool', 53.41, -2.98, '2015-01-01 00:00:00');

CREATE TABLE temperature (
    temperature_log_id serial PRIMARY KEY,
    city_id smallint,
    log_time timestamp,
    temperature real,
    CONSTRAINT fk_city
      FOREIGN KEY(city_id) 
	  REFERENCES city(city_id)
)