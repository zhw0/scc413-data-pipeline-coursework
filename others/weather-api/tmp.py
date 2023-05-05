import datetime
import json
import time
from datetime import timedelta

import dateutil
import requests
from dateutil import parser
from pymongo import MongoClient
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    desc,
)
from sqlalchemy.orm import Session, declarative_base, relationship


def test():
    current_date = datetime.date(2010, 1, 1)

    for i in range(2000):
        payload = {
            "latitude": "53.48",
            "longitude": "-2.24",
            "start_date": current_date.strftime("%Y-%m-%d"),
            "end_date": current_date.strftime("%Y-%m-%d"),
            "hourly": "temperature_2m",
        }
        url = "https://archive-api.open-meteo.com/v1/archive"
        response = requests.get(url=url, params=payload)
        data = response.json()

        data = {"raw_response": data}

        col = MongoClient()["scc413"]["weather"]
        col.insert_one(data)
        print(data)

        current_date = current_date + timedelta(days=1)
        time.sleep(10)
        print(datetime.datetime.now())


def tmp():
    col = MongoClient()["scc413"]["weather"]
    i = 0
    result = []
    for item in col.find():
        del item["_id"]
        print(item)
        i += 1
        result.append(item)
    print(i)
    import json

    with open("tmp.json", "w") as f:
        json.dump(result, f)


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


engine = create_engine(
    "postgresql+psycopg2://postgres:123456@127.0.0.1:5432/weather_db", echo=True
)

with Session(engine) as session, session.begin():
    statement = session.query(City).order_by(City.timestamp_track).limit(1)
    t = session.scalars(statement=statement).all()[0]

    payload = {
        "latitude": t.latitude,
        "longitude": t.longitude,
        "start_date": t.timestamp_track.strftime("%Y-%m-%d"),
        "end_date": t.timestamp_track.strftime("%Y-%m-%d"),
        "hourly": "temperature_2m",
    }
    url = "https://archive-api.open-meteo.com/v1/archive"
    response = requests.get(url=url, params=payload)
    data = response.json()
    print(data)

    t.timestamp_track = t.timestamp_track + timedelta(days=1)
    session.commit()
