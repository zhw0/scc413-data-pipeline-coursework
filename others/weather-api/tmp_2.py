import datetime
import json

import dateutil
from dateutil import parser
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
    timestamp_track = Column(Integer)


class Temperature(Base):
    __tablename__ = "temperature"

    temperature_log_id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer)
    log_time = Column(DateTime)
    temperature = Column(Float)


engine = create_engine(
    "postgresql+psycopg2://postgres:123456@127.0.0.1:5432/weather_db", echo=True
)

# with Session(engine) as session, session.begin():
#     statement = session.query(City).order_by(City.timestamp_track).limit(1)
#     t = session.scalars(statement=statement).all()[0]
#     print(t.city_name)
#     session.commit()


with Session(engine) as session, session.begin():
    f = open("tmp.json")
    data = json.load(f)
    for item in data:
        t = item["raw_response"]["hourly"]
        for log_time, temperature in zip(t["time"], t["temperature_2m"]):
            log_time = parser.parse(log_time)
            new_record = Temperature(
                city_id=1, log_time=log_time, temperature=temperature
            )
            session.add(new_record)
    session.commit()
# t = datetime.datetime(2010, 1, 1)

# print(t.timestamp())
