import datetime

from datetime import timedelta


import pendulum
import requests
from dateutil import parser   
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import Session, declarative_base

from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.providers.mongo.hooks.mongo import MongoHook

Base = declarative_base()


class City(Base):
    __tablename__ = "city"

    city_id = Column(Integer, primary_key=True)
    city_name = Column(String(32))
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp_track = Column(DateTime)


class Temperature(Base):
    __tablename__ = "temperature"

    temperature_log_id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer)
    log_time = Column(DateTime)
    temperature = Column(Float)


@dag(
    schedule=timedelta(seconds=10),
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["weather-data-pipeline"],
    max_active_runs=1,
)
def weather_taskflow():
    @task
    def get_weather_data():
        """Fetch historical weather data.
        """
        postgres_conn = BaseHook.get_connection("weather_db").get_uri()

        engine = create_engine(postgres_conn, echo=True)

        with Session(engine) as session, session.begin():
            statement = (
                session.query(City).order_by(City.timestamp_track).limit(1)
            )
            t = session.scalars(statement=statement).all()[0]

            payload = {
                "latitude": t.latitude,
                "longitude": t.longitude,
                "start_date": t.timestamp_track.strftime("%Y-%m-%d"),
                "end_date": t.timestamp_track.strftime("%Y-%m-%d"),
                "hourly": "temperature_2m",
            }
            url = BaseHook.get_connection("weather_api").get_uri()
            url = "https://archive-api.open-meteo.com/v1/archive"
            response = requests.get(url=url, params=payload)
            data = response.json()
            data = {
                "get_time": datetime.datetime.now().strftime(
                    "%m/%d/%Y, %H:%M:%S"
                ),
                "city_id": t.city_id,
                "api_endpoint": {"url": url, "query_parameter": payload},
                "raw_response": data,
            }
            t.timestamp_track = t.timestamp_track + timedelta(days=1)
            print("city name: " + t.city_name)
            session.commit()

        return data

    @task
    def add_data_to_mongo(data):
        hook = MongoHook(conn_id="mongo_net")
        client = hook.get_conn()
        db = client["scc413"]
        current_collection = db["weather_data"]
        current_collection.insert_one(data)
        del data["_id"]
        return data

    @task
    def add_data_to_postgres(data):
        postgres_conn = BaseHook.get_connection("weather_db").get_uri()

        engine = create_engine(postgres_conn, echo=True)

        with Session(engine) as session, session.begin():
            t = data["raw_response"]["hourly"]
            for log_time, temperature in zip(t["time"], t["temperature_2m"]):
                log_time = parser.parse(log_time)
                new_record = Temperature(
                    city_id=data["city_id"],
                    log_time=log_time,
                    temperature=temperature,
                )
                session.add(new_record)
            session.commit()

    data = get_weather_data()
    data = add_data_to_mongo(data)
    data = add_data_to_postgres(data)


weather_taskflow()
