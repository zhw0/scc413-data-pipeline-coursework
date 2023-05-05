import datetime
import json
import os
import time

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


def insert_data():
    city_list = [
        "london-2014.json",
        "manchester-2014.json",
        "liverpool-2014.json",
    ]
    city_id_list = [1, 2, 3]

    for city, city_id in zip(city_list, city_id_list):
        dir = os.path.dirname(os.path.abspath(__file__))

        json_file = os.path.join(dir, city)

        f = open(json_file)

        data = json.load(f)

        col = MongoClient(host="mongo-db", port=27017)["scc413"]["weather_data"]

        engine = create_engine(
            "postgresql+psycopg2://postgres:123456@postgres-db:5432/weather_db"
        )

        for item in data:
            col.insert_one(item)

            with Session(engine) as session, session.begin():
                t = item["raw_response"]["hourly"]
                for log_time, temperature in zip(
                    t["time"], t["temperature_2m"]
                ):
                    log_time = parser.parse(log_time)
                    new_record = Temperature(
                        city_id=city_id,
                        log_time=log_time,
                        temperature=temperature,
                    )
                    session.add(new_record)
            session.commit()


if __name__ == "__main__":
    # result = []

    # current = datetime.date(2014,1,1)

    # for i in range(370):

    #     payload = {
    #             "latitude": 53.41,
    #             "longitude": -2.98,
    #             "start_date": current.strftime("%Y-%m-%d"),
    #             "end_date": current.strftime("%Y-%m-%d"),
    #             "hourly": "temperature_2m",
    #         }

    #     url = "https://archive-api.open-meteo.com/v1/archive"
    #     response = requests.get(url=url, params=payload)
    #     data = response.json()
    #     result.append(data)
    #     print(data)
    #     print(datetime.datetime.now())
    #     time.sleep(10)
    #     current = current + datetime.timedelta(days=1)

    # f = open('liverpool-2014.json', 'w')

    # json.dump(result, f, indent=4)
    insert_data()
    # f = open('liverpool-2014.json')
    # data = json.load(f)
    # result = []
    # for item in data:
    #     item = {
    #         'raw_response': item
    #     }
    #     result.append(item)
    # json.dump(result, open('tmp.json', 'w'), indent=4)
